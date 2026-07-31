# Data and Dataset Policy

## 1. Product input policy

Version 0.1 accepts a local file from the user.
The user must own the file or have permission to process it.

The project will not include a platform video downloader.
This rule reduces copyright and platform-policy risk.

## 2. Benchmark source rules

A benchmark video needs one of these permissions:

- Project-created content
- Explicit written permission
- A license that permits the test use
- Public-domain status

The dataset record must keep the permission evidence.

## 3. Dataset record

Each video record must include:

- Stable internal identifier
- Source owner
- Source URL when applicable
- Permission type
- Permission evidence
- Language
- Tutorial category
- Duration
- Speech status
- Expected steps
- Expected time ranges
- Review status

## 4. Private data

Do not commit private videos or derived frames.
Do not put private transcript text in a public issue.

Use synthetic fixtures for public tests.
Keep restricted benchmark files in an approved private location.

## 5. Generated labels

A model can propose a label.
A human must review a reference label before benchmark use.

The dataset card must state the review process.
It must also state known label limits.

## 6. Retention and removal

The dataset owner can request removal when the permission permits this request.
The project must track the affected benchmark versions.

A release report must identify the dataset version.
It must not contain the private data itself.
