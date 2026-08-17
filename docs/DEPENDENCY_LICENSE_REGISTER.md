# Dependency License Register

This register records direct dependencies that the local review editor adds.
The release process must verify each selected version again.

| Component | Tested version | Purpose | Source | License | Distribution | Notice | Review |
|---|---:|---|---|---|---|---|---|
| FastAPI | 0.135.1 | Local web adapter | `github.com/fastapi/fastapi` | MIT | Package source | Keep license notice | Accept for alpha |
| Uvicorn | 0.41.0 | Local application server | `github.com/Kludex/uvicorn` | BSD 3-Clause | Package source | Keep license notice | Accept for alpha |
| python-multipart | 0.0.22 | Video form upload | `github.com/Kludex/python-multipart` | Apache License 2.0 | Package source | Keep license and notice | Accept for alpha |
| HTTPX | 0.28.1 | Adapter integration tests | `github.com/encode/httpx` | BSD 3-Clause | Development package | Keep license notice | Accept for alpha |

The project does not copy these packages into the repository.
The installation command downloads them from their package sources.

The initial review found no license conflict with the repository license.
This record is not a complete software bill of materials.
