# data/

This folder contains the backend’s **state and persistence**.  
All important workflow states (analysis → approval → execution → reporting) are stored here.

## Files

### `latest_analysis.json`
Stores the most recent analysis produced by the LLM, including:
- `projectId`
- `applicationUrl`
- `targetType`
- `scenario` (title/kind/actions)
- `quality` (readiness score, coverage, etc.)
- findings / coverage / riskHotspots

Written by: analysis step (CLI option `1` / `2`) via `writejson(LATEST_ANALYSIS, analysis)`.

### `approved_scenario.json`
Stores the single scenario object that is approved for execution.
Written by: CLI option `4` or API `/api/approve`.

### `runs.json`
A dictionary keyed by `runId`. Each value stores the complete execution record:
- status (PASS/FAIL)
- timestamps
- error (if any)
- actionResults (per-step PASS/FAIL, duration, error)
- scenario snapshot used for the run
- report paths + screenshot path

Updated by: `upsertrun(runid, runobj)` after each run.

### `report_index.json`
A lightweight index file used to list all exported reports quickly:
```json
{ "reports": [ { "runId": "...", "json": "...", "pdf": "...", "screenshot": "...", "createdAt": "..." } ] }
