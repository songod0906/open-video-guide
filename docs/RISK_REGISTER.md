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

Review this register at each stage gate.
Add a risk when a change adds a new trust boundary.
