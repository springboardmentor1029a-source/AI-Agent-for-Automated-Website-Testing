
Screenshots

This folder contains screenshots captured during execution (Playwright runs).

What is saved
| Item | Filename pattern | When it is created | Purpose |
|------|------------------|-------------------|---------|
| Run screenshot | `run_<timestamp>_<random>.png` | After the run finishes (or right after failure) | Visual proof of the last page state: errors, popups, captcha, wrong navigation, etc. |

How it is generated

During execution, the runner calls Playwright’s screenshot API and saves the image into this folder. 

Where it is referenced
| File | Field(s) |
|------|----------|
| `reports/run_<...>.json` | `screenshot` |
| `data/report_index.json` | `reports[].screenshot` |

Cleaning policy

This folder is safe to clean anytime. Deleting screenshots will not break new runs, but older reports may point to missing screenshot paths.
