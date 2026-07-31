# Model and Dependency License Policy

## 1. Policy goal

The project must remain useful without a paid or proprietary AI service.
All selected components must permit the planned distribution and use.

## 2. Repository license

Project source uses Apache License 2.0.
This license permits commercial and noncommercial use.
It also includes an explicit patent grant.

## 3. Acceptance rules

A component can enter the default stack when:

- A reviewer approves its source license.
- A reviewer approves its model license.
- Its use restrictions match the product goal.
- Its license record includes notice requirements.
- Its license record includes the source and exact revision.
- Its license file is available.

Do not accept a component that forbids commercial use.
Do not accept a model with an unclear redistribution rule.

## 4. Preferred licenses

Preferred licenses include:

- Apache License 2.0
- MIT License
- BSD 2-Clause License
- BSD 3-Clause License

Weak copyleft libraries need a distribution review.
Strong copyleft code must stay outside the Apache-licensed core.

## 5. Initial candidate register

This table records candidates, not final approvals.
The release process must verify each exact version again.

| Component | Planned use | Known license family | Status |
|---|---|---|---|
| FFmpeg | Media inspection and extraction | LGPL or GPL build options | Review build flags |
| whisper.cpp | Local speech recognition | MIT | Candidate |
| faster-whisper | Linux speech recognition | MIT | Candidate |
| PySceneDetect | Scene detection | BSD 3-Clause | Candidate |
| OpenCV | Image and motion work | Apache 2.0 | Candidate |
| PaddleOCR | Visible text | Apache 2.0 | Candidate |
| MLX-VLM | Apple Silicon vision runtime | MIT | Candidate |
| Qwen3-VL-4B | Visual analysis | Apache 2.0 listing | Verify exact files |
| SmolVLM2 | Low-resource visual analysis | Apache 2.0 listing | Verify exact files |

## 6. FFmpeg control

FFmpeg license terms depend on build options.
The project must record the exact binary source and configuration.

The project must not distribute a binary before this review.
System installation instructions can remain separate from the package.

## 7. Model distribution

Do not commit model weights to this repository.
Download a model from its recorded source after user approval.

Show the license before the first download.
Verify the file digest after download.

## 8. Required records

A pull request that adds a component must include:

- Component name and version
- Source URL
- Source license
- Model license when applicable
- Distribution method
- Notice requirement
- Security review status
- Approval decision

## 9. Release evidence

Each release must include a machine-readable dependency list.
It must also include all necessary notices.

The release manager must compare package contents with this policy.
