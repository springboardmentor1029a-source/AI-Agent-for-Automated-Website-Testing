#!/usr/bin/env python3
import os
import re
import json
import time
import shutil
import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv

try:
    from playwright.async_api import async_playwright
except Exception:
    async_playwright = None

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
except Exception:
    A4 = None


ROOT = Path(".").resolve()
DATADIR = ROOT / "data"
ARTIFACTSDIR = ROOT / "artifacts"
REPORTSDIR = ROOT / "reports"
SCREENSHOTSDIR = ROOT / "screenshots"

LATEST_ANALYSIS = DATADIR / "latest_analysis.json"
APPROVED_SCENARIO = DATADIR / "approved_scenario.json"
RUNSFILE = DATADIR / "runs.json"              # dict keyed by runid
REPORTINDEX = DATADIR / "report_index.json"   # dict {reports: [ ... ]}


SUPPORTEDACTIONS = {
    "goto",
    "waitforselector",
    "click",
    "fill",
    "press",
    "waitfortimeout",
    "expecturlcontains",
    "expecttextvisible",
}

PROJECTS = {
    "checkout-web": "Checkout Web",
    "mobile-app": "Mobile App",
    "admin-portal": "Admin Portal",
}


def ensuredirs() -> None:
    for d in (DATADIR, ARTIFACTSDIR, REPORTSDIR, SCREENSHOTSDIR):
        d.mkdir(parents=True, exist_ok=True)

    if not RUNSFILE.exists():
        RUNSFILE.write_text(json.dumps({}, indent=2), encoding="utf-8")

    if not REPORTINDEX.exists():
        REPORTINDEX.write_text(json.dumps({"reports": []}, indent=2), encoding="utf-8")

    if not LATEST_ANALYSIS.exists():
        LATEST_ANALYSIS.write_text(json.dumps({}, indent=2), encoding="utf-8")

    if not APPROVED_SCENARIO.exists():
        APPROVED_SCENARIO.write_text(json.dumps({}, indent=2), encoding="utf-8")


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def normalizeurl(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return url
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url


def readjson(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        txt = path.read_text(encoding="utf-8").strip()
        if not txt:
            return default
        return json.loads(txt)
    except Exception:
        return default


def writejson(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def extractjsonobject(text: str) -> Dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("Empty model response.")
    cleaned = text.strip()
    cleaned = re.sub(r"^```", "", cleaned.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not m:
        raise ValueError("Could not locate JSON object in model output.")
    return json.loads(m.group(0))


class GroqClient:
    def __init__(self, apikey: str, model: str = "llama-3.3-70b-versatile"):
        self.apikey = apikey
        self.model = model
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def chattext(self, messages: List[Dict[str, str]], temperature: float = 0.2, maxtokens: int = 2200) -> str:
        headers = {"Authorization": f"Bearer {self.apikey}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": maxtokens}
        r = requests.post(self.url, headers=headers, json=payload, timeout=120)
        if not (200 <= r.status_code < 300):
            raise RuntimeError(f"Groq HTTP {r.status_code}: {r.text}")
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def chatjson(self, messages: List[Dict[str, str]], temperature: float = 0.2, maxtokens: int = 2200) -> Dict[str, Any]:
        txt = self.chattext(messages, temperature=temperature, maxtokens=maxtokens)
        rawpath = ARTIFACTSDIR / f"groq_raw_{stamp()}.txt"
        rawpath.write_text(txt, encoding="utf-8")
        return extractjsonobject(txt)


class PerplexityClient:
    def __init__(self, apikey: str, model: str = "sonar-pro"):
        self.apikey = apikey
        self.model = model
        self.url = "https://api.perplexity.ai/chat/completions"

    def chattext(self, messages: List[Dict[str, str]], temperature: float = 0.2, maxtokens: int = 2200) -> str:
        headers = {"Authorization": f"Bearer {self.apikey}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": maxtokens}
        r = requests.post(self.url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def chatjson(self, messages: List[Dict[str, str]], temperature: float = 0.2, maxtokens: int = 2200) -> Dict[str, Any]:
        txt = self.chattext(messages, temperature=temperature, maxtokens=maxtokens)
        rawpath = ARTIFACTSDIR / f"pplx_raw_{stamp()}.txt"
        rawpath.write_text(txt, encoding="utf-8")
        return extractjsonobject(txt)


def buildanalysisprompt(payload: Dict[str, Any], combinedtext: str) -> List[Dict[str, str]]:
    system = (
        "You are an expert QA analyst. Turn requirement text into structured scenarios and analysis.\n"
        "Return JSON ONLY with schema:\n"
        "{\n"
        '  "projectId": "...",\n'
        '  "applicationUrl": "...",\n'
        '  "targetType": "website" | "api",\n'
        '  "scenario": {\n'
        '    "title": "...",\n'
        '    "kind": "website" | "api",\n'
        '    "actions": [\n'
        '      {"type":"goto","url":"...","waitUntil":"domcontentloaded"},\n'
        '      {"type":"waitforselector","selector":"...","timeoutMs":15000},\n'
        '      {"type":"click","selector":"...","timeoutMs":15000},\n'
        '      {"type":"fill","selector":"...","text":"...","timeoutMs":15000},\n'
        '      {"type":"press","selector":"...","key":"Enter","timeoutMs":15000},\n'
        '      {"type":"waitfortimeout","timeoutMs":1000},\n'
        '      {"type":"expecturlcontains","text":"..."},\n'
        '      {"type":"expecttextvisible","text":"...","timeoutMs":15000}\n'
        "    ]\n"
        "  },\n"
        '  "quality": {\n'
        '    "readinessScore": 0,\n'
        '    "requirementCoveragePct": 0,\n'
        '    "filesImpacted": 0,\n'
        '    "scenarioReadiness": "Ready" | "Needs review",\n'
        '    "openClarifications": 0\n'
        "  },\n"
        '  "findings": [ {"severity":"Low|Medium|High","category":"Gap|Ambiguity|Edge","title":"...","detail":"..."} ],\n'
        '  "coverage": {"happy":0,"negative":0,"edge":0,"nonFunctional":0},\n'
        '  "riskHotspots": [ {"module":"...","risk":"Low|Medium|High","owner":"...","reason":"..."} ]\n'
        "}\n"
        "Rules:\n"
        "- Keep output valid JSON.\n"
        "- Prefer stable selectors: id/name/aria-label/data-testid.\n"
        "- Actions should be minimal and robust.\n"
    )
    user = (
        f"ProjectId: {payload.get('projectId')}\n"
        f"ApplicationUrl: {payload.get('applicationUrl')}\n"
        f"TargetType: {payload.get('targetType')}\n"
        f"RequirementText:\n{combinedtext}\n"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def get_llm():
    groqkey = (os.getenv("GROQ_API_KEY") or os.getenv("GROQAPIKEY") or "").strip()
    pplxkey = (os.getenv("PERPLEXITY_API_KEY") or os.getenv("PERPLEXITYAPIKEY") or "").strip()
    if groqkey:
        model = (os.getenv("GROQ_MODEL") or os.getenv("GROQMODEL") or "llama-3.3-70b-versatile").strip()
        return GroqClient(apikey=groqkey, model=model), "Groq"
    if pplxkey:
        model = (os.getenv("PPLX_MODEL") or os.getenv("PPLXMODEL") or "sonar-pro").strip()
        return PerplexityClient(apikey=pplxkey, model=model), "Perplexity"
    return None, None


def analyze_input(payload: Dict[str, Any], combinedtext: str) -> Dict[str, Any]:
    llm, llmname = get_llm()
    if llm is None:
        raise RuntimeError("No LLM key set. Set GROQ_API_KEY or PERPLEXITY_API_KEY in backend/.env")

    # Use dynamic prompt only for Groq, else use normal static prompt
    if llmname == "Groq":
        msgs = build_analysis_promptpayload_dynamic(payload, combinedtext, llm)
    else:
        msgs = build_analysis_prompt(payload, combinedtext)

    try:
        out = llm.chatjson(msgs, temperature=0.2, maxtokens=3200)
    except Exception:
        txt = llm.chattext(msgs, temperature=0.2, maxtokens=3200)
        out = {
            "error": "Model returned non-JSON output",
            "rawText": txt,
            "projectId": payload.get("projectId"),
            "applicationUrl": payload.get("applicationUrl"),
            "targetType": payload.get("targetType"),
        }

    out.setdefault("projectId", payload.get("projectId"))
    out.setdefault("applicationUrl", payload.get("applicationUrl"))
    out.setdefault("targetType", payload.get("targetType"))
    return out


def msv(v: Any, default: int) -> int:
    if v is None:
        return default
    try:
        return int(v)
    except Exception:
        return default


async def runactions(
    actions: List[Dict[str, Any]],
    headless: bool,
    screenshotpath: Path,
    keepbrowseropen: bool = False,
) -> Tuple[bool, str, Optional[str], List[Dict[str, Any]]]:
    if async_playwright is None:
        return False, "Playwright not installed.", "Missing playwright dependency", []

    page = None
    browser = None
    started = time.time()
    results: List[Dict[str, Any]] = []

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=headless)
            ctx = await browser.new_context()
            page = await ctx.new_page()

            for i, a in enumerate(actions, start=1):
                t = (a.get("type") or "").strip()
                if t not in SUPPORTEDACTIONS:
                    raise ValueError(f"Unsupported action type {t!r}")

                stepstarted = time.time()
                stepstatus = "PASS"
                steperr = None

                try:
                    if t == "goto":
                        await page.goto(normalizeurl(a.get("url", "")), wait_until=a.get("waitUntil", "domcontentloaded"))
                    elif t == "waitforselector":
                        await page.wait_for_selector(a.get("selector"), timeout=msv(a.get("timeoutMs"), 15000))
                    elif t == "click":
                        await page.click(a.get("selector"), timeout=msv(a.get("timeoutMs"), 15000))
                    elif t == "fill":
                        await page.fill(a.get("selector"), a.get("text", ""), timeout=msv(a.get("timeoutMs"), 15000))
                    elif t == "press":
                        await page.press(a.get("selector"), a.get("key", "Enter"), timeout=msv(a.get("timeoutMs"), 15000))
                    elif t == "waitfortimeout":
                        await page.wait_for_timeout(msv(a.get("timeoutMs"), 1000))
                    elif t == "expecturlcontains":
                        expected = a.get("text", "")
                        if expected and expected not in page.url:
                            raise AssertionError(f"Step {i} URL mismatch. Expected contains {expected!r}, got {page.url!r}")
                    elif t == "expecttextvisible":
                        txt = a.get("text", "")
                        await page.get_by_text(txt).first.wait_for(timeout=msv(a.get("timeoutMs"), 15000))
                except Exception as e:
                    stepstatus = "FAIL"
                    steperr = str(e)
                    raise
                finally:
                    durms = int((time.time() - stepstarted) * 1000)
                    results.append(
                        {
                            "idx": i,
                            "actionType": t,
                            "status": stepstatus,
                            "error": steperr,
                            "durationMs": durms,
                            "chosenLocator": a.get("selector"),
                        }
                    )

            await page.screenshot(path=str(screenshotpath), full_page=True)

            elapsed = round(time.time() - started, 2)
            actual = f"Executed {len(actions)} actions successfully in {elapsed}s."

            if keepbrowseropen and not headless:
                input("Browser kept open. Press Enter to close...")
            await browser.close()

            return True, actual, None, results

        except Exception as e:
            try:
                if page is not None:
                    await page.screenshot(path=str(screenshotpath), full_page=True)
            except Exception:
                pass

            if browser is not None:
                if keepbrowseropen and not headless:
                    print("Run failed, browser kept open for debugging.")
                    print(f"Error: {e}")
                    input("Press Enter to close browser...")
                try:
                    await browser.close()
                except Exception:
                    pass

            return False, "Execution failed.", str(e), results


def generatepdfreport(runrecord: Dict[str, Any], pdfpath: Path) -> None:
    if A4 is None:
        raise RuntimeError("reportlab not installed. Install: pip install reportlab")

    styles = getSampleStyleSheet()
    title = ParagraphStyle("T", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#1f4788"))
    h = ParagraphStyle("H", parent=styles["Heading2"], fontSize=12, textColor=colors.HexColor("#2c5aa0"))

    doc = SimpleDocTemplate(str(pdfpath), pagesize=A4, leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    story: List[Any] = []

    story.append(Paragraph("Test Execution Report", title))
    story.append(Paragraph(f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Run Summary", h))
    summarydata = [
        ["Run ID", runrecord.get("runId", "")],
        ["Project", runrecord.get("projectId", "")],
        ["Environment", runrecord.get("environment", "")],
        ["Status", runrecord.get("status", "")],
        ["Started", runrecord.get("startedAt", "")],
        ["Finished", runrecord.get("finishedAt", "")],
        ["Error", runrecord.get("error") or "None"],
    ]
    summary = Table(summarydata, colWidths=[1.5 * inch, 4.7 * inch])
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef4fb")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(summary)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Scenario", h))
    scenario = runrecord.get("scenario") or {}
    story.append(Paragraph(f"<b>Title</b>: {scenario.get('title', 'Untitled')}", styles["Normal"]))
    story.append(Spacer(1, 0.12 * inch))

    ars = runrecord.get("actionResults") or []
    if ars:
        story.append(Paragraph("Action Results", h))
        data = [["#", "Action", "Status", "Duration (ms)", "Error"]]
        for a in ars:
            data.append(
                [
                    str(a.get("idx", "")),
                    str(a.get("actionType", "")),
                    str(a.get("status", "")),
                    str(a.get("durationMs", 0)),
                    (a.get("error") or "")[:120],
                ]
            )
        tbl = Table(data, colWidths=[0.4 * inch, 1.3 * inch, 0.8 * inch, 1.0 * inch, 2.8 * inch])
        tbl.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#208078")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(tbl)
        story.append(Spacer(1, 0.2 * inch))

    screenshot = runrecord.get("screenshot")
    if screenshot and Path(screenshot).exists():
        story.append(Paragraph("Screenshot", h))
        try:
            story.append(RLImage(screenshot, width=6.2 * inch, height=3.6 * inch))
        except Exception as e:
            story.append(Paragraph(f"Could not embed screenshot: {e}", styles["Normal"]))

    doc.build(story)


def upsertrun(runid: str, runobj: Dict[str, Any]) -> None:
    runs = readjson(RUNSFILE, {})
    if not isinstance(runs, dict):
        runs = {}
    runs[runid] = runobj
    writejson(RUNSFILE, runs)


def registerreport(runid: str, jsonreport: Path, pdfreport: Optional[Path], screenshotpath: Optional[Path]) -> None:
    idx = readjson(REPORTINDEX, {"reports": []})
    if not isinstance(idx, dict):
        idx = {"reports": []}
    if "reports" not in idx or not isinstance(idx["reports"], list):
        idx["reports"] = []

    idx["reports"].append(
        {
            "runId": runid,
            "json": str(jsonreport),
            "pdf": str(pdfreport) if pdfreport else None,
            "screenshot": str(screenshotpath) if screenshotpath else None,
            "createdAt": datetime.now().isoformat(),
        }
    )
    writejson(REPORTINDEX, idx)


def promptmultiline(label: str) -> str:
    print(label)
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()


def cli_menu() -> None:
    load_dotenv()
    ensuredirs()

    while True:
        print("-" * 70)
        print("AI Test Automation - Menu Driven CLI")
        print("-" * 70)
        print("1  Data Input Text")
        print("2  Data Input Files/ZIP (store as artifact)")
        print("3  Analysis Review View latest")
        print("4  Send to Test Console Approve")
        print("5  Test Console Run approved")
        print("6  Execution Dashboard List runs")
        print("7  Reports List export paths")
        print("8  Start Web Server (FastAPI)")
        print("9  Exit")
        choice = input("> ").strip()

        if choice == "1":
            print("Project ids:", ", ".join(PROJECTS.keys()))
            projectid = input("Project id: ").strip() or "checkout-web"
            appurl = input("Application URL: ").strip()
            targettype = (input("Target type website/api: ").strip().lower() or "website")
            reqtext = promptmultiline("Requirement text (multi-line). Press Enter on empty line to finish:")

            payload = {"projectId": projectid, "applicationUrl": normalizeurl(appurl), "targetType": targettype}
            analysis = analyze_input(payload, reqtext)
            writejson(LATEST_ANALYSIS, analysis)
            print(f"Saved latest analysis -> {LATEST_ANALYSIS}")

        elif choice == "2":
            print("Project ids:", ", ".join(PROJECTS.keys()))
            projectid = input("Project id: ").strip() or "checkout-web"
            appurl = input("Application URL: ").strip()
            targettype = (input("Target type website/api: ").strip().lower() or "website")
            filepath = input("Path to file/zip/folder: ").strip()
            p = Path(filepath)
            if not p.exists():
                print("File not found.")
                continue

            dest = ARTIFACTSDIR / f"input_{stamp()}_{p.name}"
            if p.is_dir():
                shutil.make_archive(str(dest), "zip", root_dir=str(p))
                combined = f"Folder uploaded: {p} -> {dest}.zip"
            else:
                shutil.copy2(p, dest)
                combined = f"File uploaded: {dest.name}"

            payload = {"projectId": projectid, "applicationUrl": normalizeurl(appurl), "targetType": targettype}
            analysis = analyze_input(payload, combined)
            writejson(LATEST_ANALYSIS, analysis)
            print(f"Saved latest analysis -> {LATEST_ANALYSIS}")

        elif choice == "3":
            print(LATEST_ANALYSIS.read_text(encoding="utf-8"))

        elif choice == "4":
            analysis = readjson(LATEST_ANALYSIS, {})
            scenario = analysis.get("scenario")
            if not isinstance(scenario, dict):
                print("Latest analysis does not contain a structured scenario.")
                continue
            writejson(APPROVED_SCENARIO, scenario)
            print(f"Approved scenario saved -> {APPROVED_SCENARIO}")

        elif choice == "5":
            scenario = readjson(APPROVED_SCENARIO, {})
            actions = scenario.get("actions") if isinstance(scenario, dict) else None
            if not actions:
                print("No approved scenario/actions. Use option 4 first.")
                continue

            headless = (os.getenv("HEADLESS", "true").strip().lower() != "false")
            keepopenenv = (os.getenv("KEEP_BROWSER_OPEN", "false").strip().lower() == "true")
            keepbrowseropen = keepopenenv
            if not headless:
                ans = input("Keep browser open after run? yN ").strip().lower()
                if ans in ("y", "yes"):
                    keepbrowseropen = True

            runid = f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(3).hex()}"
            screenshotpath = SCREENSHOTSDIR / f"{runid}.png"
            startedat = datetime.now().isoformat()

            ok, actual, err, actionresults = asyncio.run(
                runactions(actions, headless=headless, screenshotpath=screenshotpath, keepbrowseropen=keepbrowseropen)
            )

            finishedat = datetime.now().isoformat()
            status = "PASS" if ok else "FAIL"

            latest = readjson(LATEST_ANALYSIS, {})
            projectid = latest.get("projectId") or "checkout-web"

            jsonreportpath = REPORTSDIR / f"{runid}.json"
            pdfreportpath = REPORTSDIR / f"{runid}.pdf"

            runobj: Dict[str, Any] = {
                "runId": runid,
                "projectId": projectid,
                "environment": "Chrome headless" if headless else "Chrome",
                "runType": "full-execution",
                "status": status,
                "startedAt": startedat,
                "finishedAt": finishedat,
                "error": err,
                "actionResults": actionresults,
                "scenario": scenario,
                "actualResult": actual,
                "screenshot": str(screenshotpath) if screenshotpath.exists() else None,
                "reportPaths": {"json": str(jsonreportpath), "pdf": str(pdfreportpath) if A4 is not None else None},
            }

            writejson(jsonreportpath, runobj)

            pdfok = False
            if A4 is not None:
                try:
                    generatepdfreport(runobj, pdfreportpath)
                    pdfok = True
                except Exception as e:
                    runobj["reportPaths"]["pdf"] = None
                    runobj["pdfError"] = str(e)
                    writejson(jsonreportpath, runobj)

            upsertrun(runid, runobj)
            registerreport(runid, jsonreportpath, pdfreportpath if pdfok else None, screenshotpath if screenshotpath.exists() else None)

            print(json.dumps({k: runobj.get(k) for k in ("runId", "status", "startedAt", "finishedAt", "error")}, indent=2))
            print(f"Report JSON saved: {jsonreportpath}")
            print(f"Report PDF saved:  {pdfreportpath if pdfok else 'Not generated'}")

        elif choice == "6":
            runs = readjson(RUNSFILE, {})
            if not runs:
                print("No runs yet.")
                continue
            for runid, r in list(runs.items())[-20:]:
                title = ((r.get("scenario") or {}).get("title")) if isinstance(r, dict) else ""
                print(f"- {runid}  {r.get('status')}  {title}  {r.get('startedAt')}")

        elif choice == "7":
            idx = readjson(REPORTINDEX, {"reports": []})
            reps = idx.get("reports") if isinstance(idx, dict) else []
            if not reps:
                print("No reports yet.")
                continue
            for r in reps[-30:]:
                print(f"- runId: {r.get('runId')}")
                print(f"  json: {r.get('json')}")
                print(f"  pdf:  {r.get('pdf')}")
                print(f"  screenshot: {r.get('screenshot')}")

        elif choice == "8":
            start_fastapi_server()

        elif choice == "9":
            print("Bye.")
            return

        else:
            print("Invalid option.")


def start_fastapi_server() -> None:
    ensuredirs()
    load_dotenv()

    try:
        from fastapi import FastAPI, UploadFile, File
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.staticfiles import StaticFiles
        from pydantic import BaseModel
        import uvicorn
    except Exception:
        print("FastAPI/uvicorn not installed. Install: pip install fastapi uvicorn pydantic")
        return

    app = FastAPI(title="AI Test Automation Server")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/files/reports", StaticFiles(directory=str(REPORTSDIR)), name="reports")
    app.mount("/files/screenshots", StaticFiles(directory=str(SCREENSHOTSDIR)), name="screenshots")
    app.mount("/files/artifacts", StaticFiles(directory=str(ARTIFACTSDIR)), name="artifacts")

    class AnalyzeRequest(BaseModel):
        projectId: str
        applicationUrl: str
        targetType: str = "website"
        requirementText: str

    class ApproveRequest(BaseModel):
        scenario: Dict[str, Any]

    class RunRequest(BaseModel):
        headless: bool = True
        keepBrowserOpen: bool = False

    @app.get("/api/health")
    def health():
        return {"status": "ok", "time": datetime.now().isoformat()}

    @app.get("/api/analysis/latest")
    def api_latest_analysis():
        return readjson(LATEST_ANALYSIS, {})

    @app.post("/api/analyze")
    def api_analyze(req: AnalyzeRequest):
        payload = {
            "projectId": req.projectId,
            "applicationUrl": normalizeurl(req.applicationUrl),
            "targetType": req.targetType,
        }
        analysis = analyze_input(payload, req.requirementText)
        writejson(LATEST_ANALYSIS, analysis)
        return analysis

    @app.post("/api/analyze/upload")
    async def api_analyze_upload(
        projectId: str,
        applicationUrl: str,
        targetType: str = "website",
        file: UploadFile = File(...),
    ):
        ensuredirs()
        fname = f"upload_{stamp()}_{file.filename}"
        dest = ARTIFACTSDIR / fname
        content = await file.read()
        dest.write_bytes(content)

        payload = {"projectId": projectId, "applicationUrl": normalizeurl(applicationUrl), "targetType": targetType}
        combinedtext = f"Uploaded file saved as {fname}. Use it as context to generate scenario."
        analysis = analyze_input(payload, combinedtext)
        writejson(LATEST_ANALYSIS, analysis)
        return analysis

    @app.get("/api/scenario/approved")
    def api_get_approved():
        return readjson(APPROVED_SCENARIO, {})

    @app.post("/api/approve")
    def api_approve(req: ApproveRequest):
        if not isinstance(req.scenario, dict):
            raise ValueError("scenario must be an object")
        writejson(APPROVED_SCENARIO, req.scenario)
        return {"status": "ok", "approvedScenarioPath": str(APPROVED_SCENARIO)}

    @app.post("/api/run")
    def api_run(req: RunRequest):
        scenario = readjson(APPROVED_SCENARIO, {})
        actions = scenario.get("actions") if isinstance(scenario, dict) else None
        if not actions:
            return {"status": "error", "message": "No approved scenario/actions. Call /api/approve first."}

        runid = f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(3).hex()}"
        screenshotpath = SCREENSHOTSDIR / f"{runid}.png"
        startedat = datetime.now().isoformat()

        ok, actual, err, actionresults = asyncio.run(
            runactions(actions, headless=req.headless, screenshotpath=screenshotpath, keepbrowseropen=req.keepBrowserOpen)
        )

        finishedat = datetime.now().isoformat()
        status = "PASS" if ok else "FAIL"

        latest = readjson(LATEST_ANALYSIS, {})
        projectid = latest.get("projectId") or "checkout-web"

        jsonreportpath = REPORTSDIR / f"{runid}.json"
        pdfreportpath = REPORTSDIR / f"{runid}.pdf"

        runobj: Dict[str, Any] = {
            "runId": runid,
            "projectId": projectid,
            "environment": "Chrome headless" if req.headless else "Chrome",
            "runType": "full-execution",
            "status": status,
            "startedAt": startedat,
            "finishedAt": finishedat,
            "error": err,
            "actionResults": actionresults,
            "scenario": scenario,
            "actualResult": actual,
            "screenshot": str(screenshotpath) if screenshotpath.exists() else None,
            "reportPaths": {"json": str(jsonreportpath), "pdf": str(pdfreportpath) if A4 is not None else None},
        }

        writejson(jsonreportpath, runobj)

        pdfok = False
        if A4 is not None:
            try:
                generatepdfreport(runobj, pdfreportpath)
                pdfok = True
            except Exception as e:
                runobj["reportPaths"]["pdf"] = None
                runobj["pdfError"] = str(e)
                writejson(jsonreportpath, runobj)

        upsertrun(runid, runobj)
        registerreport(runid, jsonreportpath, pdfreportpath if pdfok else None, screenshotpath if screenshotpath.exists() else None)

        return {
            "status": "ok",
            "run": runobj,
            "files": {
                "reportJsonUrl": f"/files/reports/{runid}.json",
                "reportPdfUrl": f"/files/reports/{runid}.pdf" if pdfok else None,
                "screenshotUrl": f"/files/screenshots/{runid}.png" if screenshotpath.exists() else None,
            },
        }

    @app.get("/api/runs")
    def api_runs():
        return readjson(RUNSFILE, {})

    @app.get("/api/reports")
    def api_reports():
        return readjson(REPORTINDEX, {"reports": []})

    print("Starting FastAPI on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

from urllib.parse import urlparse

def _domain_from_url(url: str) -> str:
    try:
        u = urlparse(url.strip())
        return (u.netloc or "").lower()
    except Exception:
        return ""

def build_dynamic_prompt_with_groq(
    groq: "GroqClient",
    application_url: str,
    target_type: str = "website",
) -> str:
    domain = _domain_from_url(application_url)

    system_meta = (
        "You create system prompts for a Playwright-style test action generator. "
        "Output ONLY the system prompt text (no JSON, no markdown, no quotes). "
        "The prompt MUST be general-purpose and robust across websites."
    )

    user_meta = f"""
Target: {target_type}
Application URL: {application_url}
Domain: {domain}

Generate a system prompt that forces the model to:
- Return JSON ONLY with schema: projectid, applicationurl, targettype, scenario{{title,kind,actions}}, quality, findings, coverage, riskhotspots
- Use ONLY these action types: goto, waitforselector, click, fill, press, waitfortimeout, expecturlcontains, expecttextvisible
- Prefer stable selectors (data-testid/data-test/data-cy, aria-label, name, placeholder, unique id)
- Avoid brittle selectors (deep CSS chains, nth-child, generated classes, ambiguous ids)
- For every interactive action (click/fill/press), generate 1 primary selector AND 1–3 fallbacks using a "selectors": [...] array
- Always add waitforselector before click/fill/press using the same selector(s)
- Add site-aware hints only if needed (based on domain), but do not hardcode a single site; keep it general.
"""

    txt = groq.chattext(
        messages=[
            {"role": "system", "content": system_meta},
            {"role": "user", "content": user_meta},
        ],
        temperature=0.2,
        maxtokens=900,
    )
    return txt.strip()


def build_analysis_promptpayload_dynamic(
    payload: Dict[str, Any],
    combinedtext: str,
    groq: "GroqClient",
) -> List[Dict[str, str]]:
    # Step 1: get a site-aware system prompt
    dyn_system = build_dynamic_prompt_with_groq(
        groq=groq,
        application_url=payload.get("applicationurl", ""),
        target_type=payload.get("targettype", "website"),
    )

    # Step 2: use that system prompt to generate the actual scenario JSON
    user = (
        f"Project: {payload.get('projectid')}\n"
        f"Application URL: {payload.get('applicationurl')}\n"
        f"Target type: {payload.get('targettype')}\n"
        f"Requirement text:\n{combinedtext}\n"
        f"Return JSON only."
    )

    return [
        {"role": "system", "content": dyn_system},
        {"role": "user", "content": user},
    ]


if __name__ == "__main__":
    cli_menu()
