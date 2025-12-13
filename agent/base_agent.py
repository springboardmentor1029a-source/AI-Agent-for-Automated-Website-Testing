from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
import re, os, time, uuid
from datetime import datetime

# State schema 
class AgentState(TypedDict, total=False):
    instruction: str
    target: str
    steps: List[dict]
    status: str
    error: Optional[str]
    mode: Optional[str]               # "simulate" or "execute"
    step_results: Optional[List[dict]]
    duration_sec: Optional[float]


# Website Mapping
KNOWN_SITES = {
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "myntra": "https://www.myntra.com",
    "meesho": "https://www.meesho.com",
}


# Helper: detect full URLs 
def extract_url(text: str) -> Optional[str]:
    url_pattern = r"(https?://[^\s]+)"
    match = re.search(url_pattern, text)
    return match.group(1) if match else None


# Helper: extract search query robustly 
def extract_search_query(text: str, site_hint: Optional[str] = None) -> Optional[str]:
    if not text:
        return None
    quoted = re.findall(r'["\'](.+?)["\']', text)
    if quoted:
        return quoted[0].strip()
    lowered = text.lower()
    patterns = [
        r'(?:open\s+\w+\s+and\s+)?(?:search(?:\s+for)?|find|look for|look for)\s+(.+)$',
        r'(?:check|check if|is there|is)?\s*(?:there\s+)?(?:any\s+)?(?:results\s+for\s+)?(.+)$',
        r'(?:search:)\s*(.+)$',
    ]
    for pat in patterns:
        m = re.search(pat, lowered, flags=re.I)
        if m:
            q = m.group(1).strip()
            for site in KNOWN_SITES.keys():
                q = re.sub(r'^\b' + re.escape(site) + r'\b', '', q).strip()
            q = re.sub(r'^(and|open|the)\b', '', q).strip()
            q = re.sub(r'\b(available|availability|please|now)\b$', '', q).strip()
            q = q.strip(' .?')
            if q:
                return q
    words = lowered.split()
    if len(words) <= 1:
        return None
    leading_commands = {"open", "go", "visit", "check", "search", "find", "look", "for", "is", "are"}
    while words and words[0] in leading_commands:
        words.pop(0)
    if not words:
        return None
    return " ".join(words).strip()


# Node 1: Receive 
def receive_node(state: AgentState) -> AgentState:
    instr = state.get("instruction", "") or ""
    target = state.get("target", "") or ""
    state["instruction"] = instr.strip()
    state["target"] = target.strip()
    state.setdefault("mode", "simulate")
    state["status"] = "received"
    return state


# Node 2: Parse 
def parse_instruction_node(state: AgentState) -> AgentState:
    instr = state.get("instruction", "") or ""
    lowered = instr.lower()
    steps: List[dict] = []
    full_url = extract_url(instr)
    matched_site = None

    # navigation step resolution
    if full_url:
        steps.append({"action": "goto", "target": full_url, "detail": f"navigate to {full_url}"})
        state["target"] = full_url
    else:
        for word, url in KNOWN_SITES.items():
            if re.search(r'\b' + re.escape(word) + r'\b', lowered):
                steps.append({"action": "goto", "target": url, "detail": f"navigate to {url}"})
                state["target"] = url
                matched_site = word
                break
        if not matched_site:
            t = state.get("target", "")
            if isinstance(t, str) and t.startswith("/"):
                steps.append({"action": "goto", "target": t, "detail": f"navigate to {t}"})
            else:
                steps.append({"action": "clarify", "detail": "Unclear navigation target."})

    # quoted values
    quoted = re.findall(r'["\'](.+?)["\']', instr)
    if "name" in lowered and quoted:
        steps.append({"action": "type", "selector": "input#name", "value": quoted[0], "detail": f"type '{quoted[0]}' in #name"})

    # generic "type X into Y"
    m = re.search(r"type\s+(.+?)\s+(?:in|into)\s+([A-Za-z0-9_\- ]+)", instr, re.I)
    if m:
        val = m.group(1).strip()
        field = m.group(2).strip().replace(" ", "_")
        selector = f"input#{field}"
        steps.append({"action": "type", "selector": selector, "value": val, "detail": f"type '{val}' into {selector}"})

    # site-specific search
    if matched_site == "amazon" or (isinstance(state.get("target", ""), str) and "amazon" in state.get("target", "").lower()):
        query = quoted[0].strip() if quoted else extract_search_query(instr, "amazon")
        if query:
            steps.append({"action": "type", "selector": "input[id='twotabsearchtextbox']", "value": query, "detail": f"search Amazon for '{query}'"})
            steps.append({"action": "click", "selector": "input[id='nav-search-submit-button']", "detail": "submit Amazon search"})

    if matched_site == "google" or (isinstance(state.get("target", ""), str) and "google" in state.get("target", "").lower()):
        query = quoted[0].strip() if quoted else extract_search_query(instr, "google")
        if query:
            steps.append({"action": "type", "selector": "input[name='q']", "value": query, "detail": f"search Google for '{query}'"})
            steps.append({"action": "press_enter", "detail": "submit Google search by pressing Enter"})

    # generic click
    if any(k in lowered for k in ("click", "submit", "press")) and not any(s.get("action") == "click" for s in steps):
        steps.append({"action": "click", "selector": "button, input[type=submit], input[type=button]", "detail": "click button"})

    if not steps:
        steps.append({"action": "clarify", "detail": "Could not parse instruction."})

    state["steps"] = steps
    state["status"] = "parsed"
    return state


# Node 3: Execute (very robust for Google/Amazon) 
def execute_steps_node(state: AgentState) -> AgentState:
    steps = state.get("steps", []) or []
    mode = state.get("mode", "simulate")
    results: List[dict] = []

    screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "screenshots"))
    os.makedirs(screenshots_dir, exist_ok=True)
    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:6]

    if mode != "execute":
        for i, s in enumerate(steps, start=1):
            results.append({"step": i, "action": s.get("action"), "detail": s.get("detail"), "status": "simulated", "screenshot": None})
        state["step_results"] = results
        state["status"] = "completed_simulated"
        return state

    # Execution with Playwright
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
    except Exception as e:
        state["error"] = f"Playwright import error: {e}"
        state["status"] = "error"
        return state

    start_time = time.time()
    try:
        with sync_playwright() as p:
            # CONFIG 
            HEADLESS = True       # set False while debugging to watch the browser
            SLOW_MO = 0           # e.g., 120 to slow actions for debugging
            launch_args = ["--no-sandbox", "--disable-dev-shm-usage"]
            # LAUNCH 
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO, args=launch_args)
            user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            context = browser.new_context(user_agent=user_agent, locale="en-GB", timezone_id="Asia/Kolkata", accept_downloads=True, viewport={"width":1280,"height":800})
            stealth_script = "Object.defineProperty(navigator, 'webdriver', {get: () => false});"
            context.add_init_script(stealth_script)
            try:
                context.set_extra_http_headers({"accept-language":"en-GB,en;q=0.9"})
            except Exception:
                pass
            page = context.new_page()
            page.set_default_timeout(45000)

            # helper: try to type robustly
            def robust_type(page, value, selectors):
                """
                selectors: list of css selectors (strings) to try in order.
                Returns (ok, used_selector, detail)
                """
                # try each selector
                for sel in selectors:
                    try:
                        page.wait_for_selector(sel, timeout=7000)
                    except Exception:
                        continue
                    # if element exists attempt fill
                    try:
                        page.fill(sel, value)
                        return True, sel, f"typed '{value}' into {sel}"
                    except Exception:
                        # fallback focus + keyboard
                        try:
                            page.focus(sel)
                            page.keyboard.type(value, delay=30)
                            return True, sel, f"keyboard-typed '{value}' into {sel}"
                        except Exception:
                            # fallback JS set
                            try:
                                page.evaluate("(sel,val)=>{ const e=document.querySelector(sel); if(e){ e.value=val; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); } }", sel, value)
                                return True, sel, f"js-set '{value}' into {sel}"
                            except Exception:
                                continue
                # last-resort: search visible inputs and try to set the best one
                try:
                    inputs = page.query_selector_all("input, textarea")
                    # choose visible inputs with reasonable size
                    candidates = []
                    for el in inputs:
                        try:
                            visible = el.is_visible()
                            if not visible:
                                continue
                            typ = el.get_attribute("type") or ""
                            maxlength = el.get_attribute("maxlength") or ""
                            candidates.append((typ, maxlength, el))
                        except Exception:
                            continue
                    # pick first candidate
                    if candidates:
                        el = candidates[0][2]
                        try:
                            # focus then set via keyboard
                            el.focus()
                            page.keyboard.type(value, delay=30)
                            return True, "visible-input-picked", f"keyboard-typed into picked visible input"
                        except Exception:
                            try:
                                page.evaluate("(el, val)=>{ el.value=val; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true})); }", el, value)
                                return True, "visible-input-picked-js", "js-set into picked visible input"
                            except Exception:
                                return False, None, "failed to set value on visible inputs"
                    else:
                        return False, None, "no visible inputs found"
                except Exception as e:
                    return False, None, f"exception while locating visible inputs: {e}"

            # execution loop
            step_no = 0
            last_step_ok = True
            for s in steps:
                step_no += 1
                action = s.get("action")
                try:
                    if action == "goto":
                        url = s.get("target", state.get("target", "/test"))
                        if isinstance(url,str) and url.startswith("/"):
                            url = "http://127.0.0.1:5000" + url
                        page.goto(url, wait_until="networkidle", timeout=60000)
                        page.wait_for_timeout(1200)
                        detail = f"navigated to {url}"
                        last_step_ok = True

                        # attempt to close common overlays (Google consent etc.)
                        if "google." in url:
                            consent_selectors = ["form[action*='consent'] button", "#L2AGLb", "button[aria-label='Accept all']", "button[aria-label='I agree']"]
                            for cs in consent_selectors:
                                try:
                                    el = page.query_selector(cs)
                                    if el:
                                        try:
                                            el.click()
                                            page.wait_for_timeout(700)
                                            break
                                        except Exception:
                                            pass
                                except Exception:
                                    pass

                    elif action == "type":
                        selector = s.get("selector", "input")
                        value = s.get("value", "")
                        # build selectors list
                        selectors = [selector]
                        if selector in ("input[name='q']", "input[id='twotabsearchtextbox']"):
                            selectors += ["input[title='Search']", "input[aria-label='Search']", "input[type='search']", "input.gsfi"]
                        ok, used_sel, detail_msg = robust_type(page, value, selectors)
                        if not ok:
                            results.append({"step": step_no, "action": action, "detail": f"Failed to type: tried selectors {selectors}; fallback: {detail_msg}", "status": "error", "screenshot": None})
                            last_step_ok = False
                            continue
                        else:
                            detail = detail_msg
                            last_step_ok = True

                    elif action == "click":
                        selector = s.get("selector", "button")
                        try:
                            page.wait_for_selector(selector, timeout=45000)
                            try:
                                page.click(selector)
                            except Exception:
                                page.evaluate("(sel)=>{ const el=document.querySelector(sel); if(el) el.click(); }", selector)
                            page.wait_for_timeout(600)
                            detail = f"clicked {selector}"
                            last_step_ok = True
                        except Exception as e:
                            results.append({"step": step_no, "action": action, "detail": f"click failed on {selector}: {e}", "status": "error", "screenshot": None})
                            last_step_ok = False
                            continue

                    elif action == "press_enter":
                        # If previous typing failed, try to salvage by focusing first visible input
                        if not last_step_ok:
                            # try to focus first visible input and then press Enter
                            try:
                                inputs = page.query_selector_all("input, textarea")
                                focused = False
                                for el in inputs:
                                    try:
                                        if el.is_visible():
                                            el.focus()
                                            page.wait_for_timeout(200)
                                            focused = True
                                            break
                                    except Exception:
                                        continue
                                if not focused:
                                    # fallback: focus body
                                    page.evaluate("()=>{ document.body.focus(); }")
                                page.keyboard.press("Enter")
                                page.wait_for_timeout(1000)
                                results.append({"step": step_no, "action": action, "detail": "pressed Enter after fallback focus", "status": "ok", "screenshot": None})
                                last_step_ok = True
                                continue
                            except Exception as e:
                                results.append({"step": step_no, "action": action, "detail": f"skipped Enter - previous typing failed and fallback also failed: {e}", "status": "skipped", "screenshot": None})
                                last_step_ok = False
                                continue
                        # normal path
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(1000)
                        detail = "pressed Enter key"
                        last_step_ok = True

                    elif action == "clarify":
                        detail = "clarify - cannot execute"
                        last_step_ok = False

                    else:
                        detail = f"unknown action {action}"
                        last_step_ok = False

                    # screenshot
                    fname = f"{run_id}_step{step_no}.png"
                    fp = os.path.join(screenshots_dir, fname)
                    try:
                        page.screenshot(path=fp, full_page=False)
                        screenshot_rel = os.path.relpath(fp, start=os.path.join(os.path.dirname(__file__), "..", "static"))
                    except Exception:
                        screenshot_rel = None

                    results.append({"step": step_no, "action": action, "detail": detail, "status": "ok" if last_step_ok else "error", "screenshot": screenshot_rel})

                except PWTimeoutError as te:
                    results.append({"step": step_no, "action": action, "detail": str(te), "status": "timeout", "screenshot": None})
                    last_step_ok = False
                except Exception as e:
                    results.append({"step": step_no, "action": action, "detail": str(e), "status": "error", "screenshot": None})
                    last_step_ok = False

            try:
                browser.close()
            except Exception:
                pass

        state["step_results"] = results
        state["status"] = "executed"
        state["duration_sec"] = round(time.time() - start_time, 3)
        return state

    except Exception as e:
        state["error"] = str(e)
        state["status"] = "error"
        return state


# Node 4: Finalize 
def finalize_node(state: AgentState) -> AgentState:
    return state


# Build Graph 
def create_agent():
    graph = StateGraph(AgentState)
    graph.add_node("receive", receive_node)
    graph.add_node("parse", parse_instruction_node)
    graph.add_node("execute", execute_steps_node)
    graph.add_node("finalize", finalize_node)
    graph.add_edge(START, "receive")
    graph.add_edge("receive", "parse")
    graph.add_edge("parse", "execute")
    graph.add_edge("execute", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()
