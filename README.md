# **AI-Agent-for-Automated-Website-Testing**

An AI-assisted test automation system that converts plain-English requirements into executable website test scenarios, runs them in a browser, and stores reports and screenshots for review. 

What this project is
This project provides an end-to-end workflow to generate, review, approve, and execute automated website tests using an LLM-driven scenario generator and a browser automation runner. 

How the system works
| Stage | What happens | Output produced |
|------|--------------|----------------|
| Analyze | Requirement input is converted into a structured scenario with executable actions | Latest analysis saved for review |
| Approve | A reviewed scenario is marked as ready to execute | Approved scenario saved |
| Execute | Browser automation runs the actions step-by-step | Step results + screenshot evidence |
| Report | Results are exported and indexed | JSON/PDF exports and run history |

Repository layout
| Folder | Responsibility |
|--------|----------------|
| backend/ | Scenario generation, execution engine, persistence layer, report generation, and API server |
| frontend/ | User interface to submit inputs, review analysis, approve scenarios, run tests, and view reports |

Backend overview
The backend manages the complete automation pipeline: analysis generation, scenario approval, action execution, and report export. 

Backend data & storage
| Location | Stored content | Why it exists |
|----------|----------------|---------------|
| backend/artifacts/ | Raw LLM outputs and uploaded artifacts | Debugging and traceability for generated scenarios |
| backend/data/ | Latest analysis, approved scenario, runs history, report index | Persistent workflow state across executions |
| backend/reports/ | Run exports (JSON always, PDF when enabled) | Shareable execution outputs |
| backend/screenshots/ | Browser screenshots captured during runs | Visual evidence for failures and final state |

Backend lifecycle states
| File | Meaning |
|------|---------|
| backend/data/latest_analysis.json | Latest AI-generated analysis and scenario |
| backend/data/approved_scenario.json | Scenario that has been approved for execution |
| backend/data/runs.json | Historical run records keyed by run id |
| backend/data/report_index.json | A listing index for exported reports and screenshots |

Frontend overview
The frontend provides a clean UI to navigate the automation workflow without using the CLI. It focuses on data input, analysis review, approvals, execution monitoring, and report browsing. 

End-to-end user journey
| User action | System response |
|------------|------------------|
| Provide a requirement | Scenario is generated and stored for review |
| Review and approve | Scenario is persisted as approved |
| Run approved scenario | Execution starts and produces screenshots + per-step results |
| Open reports | JSON/PDF exports and run history are available for review |

Key outputs you can expect
| Output | Where it appears | What it is used for |
|--------|------------------|---------------------|
| Raw model output | backend/artifacts/ | Debugging and transparency of AI generation |
| Latest analysis | backend/data/latest_analysis.json | Review before approval |
| Approved scenario | backend/data/approved_scenario.json | Single source of truth for execution |
| Run report (JSON) | backend/reports/ | Machine-readable execution details |
| Run report (PDF) | backend/reports/ | Human-friendly report (optional) |
| Screenshot evidence | backend/screenshots/ | Visual proof of execution state |

Scope and limitations
This project focuses on deterministic action execution based on generated selectors/actions; real-world sites may block automation through captchas or bot checks, which can prevent reliable execution. 
