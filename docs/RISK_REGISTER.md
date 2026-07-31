# Risk Register

| ID | Risk | Probability | Effect | Control | Owner |
|---|---|---:|---:|---|---|
| R-01 | The model invents a step | High | High | Require evidence and verification | AI engineer |
| R-02 | Silent video quality is low | High | High | Use motion, text, and dense samples | AI engineer |
| R-03 | Local inference is too slow | Medium | High | Use profiles, caching, and benchmarks | Technical lead |
| R-04 | A license blocks distribution | Medium | High | Review exact versions before merge | Release manager |
| R-05 | User media leaves the computer | Low | Critical | Keep local mode as the default | Security reviewer |
| R-06 | A decoder processes hostile media | Medium | High | Isolate media work and patch dependencies | Security reviewer |
| R-07 | An integration changes its contract | Medium | Medium | Use adapters and a version matrix | Software engineer |
| R-08 | Public hosting creates high cost | High | High | Do not promise a free hosted service | Product owner |
| R-09 | A guide redistributes protected content | Medium | High | Use user-owned input and attribution | Product owner |
| R-10 | Technical text does not obey STE | Medium | Medium | Use checks and trained review | Technical writer |
| R-11 | Confidence is not calibrated | Medium | High | Measure calibration on held-out data | AI engineer |
| R-12 | An MCP tool exposes a private job | Low | Critical | Enforce ownership in the service | Security reviewer |
| R-13 | One reviewer introduces annotation bias | High | Medium | Require two reviewers before benchmark scoring | AI engineer |
| R-14 | A generated physical guide causes injury | Medium | Critical | Add warnings and exclude safety certification | Product owner |
| R-15 | An MCP client requests an unauthorized local path | Medium | Critical | Require approved input and output roots | Security reviewer |
| R-16 | A model download uses excessive storage or network data | Medium | Medium | Show model size and keep a small default | AI engineer |
| R-17 | A job overwrites files from another application | Low | High | Require a product marker in a reused output directory | Software engineer |
| R-18 | A test driver performs an unintended administration call | Low | High | Bind locally and use fixed test actions | Software engineer |
| R-19 | Local jobs use excessive storage | Medium | High | Limit uploads and show stored job sizes | Software engineer |
| R-20 | Another website sends a local editor command | Medium | High | Check the host and write-request origin | Security reviewer |
| R-21 | An agent uses stale project context | Medium | High | Refresh from Git and keep one project state | Technical lead |

Review this register at each stage gate.
Add a risk when a change adds a new trust boundary.
