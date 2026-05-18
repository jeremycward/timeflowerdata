# timeflowerdata

Language-agnostic schema repository for timeflower timeline data.

## Repository contents

- `timelineschema.json` — source JSON Schema
- `python/generate_pydantic_models.py` — build script that generates Python (Pydantic) artifacts from the schema
- `python/src/timeflowerdata_schema/` — Python package source for distributable schema models
- `.github/workflows/release_schema.yml` — manual GitHub Action that builds and publishes versioned package artifacts to GitHub Releases

Generated artifacts are intentionally not stored in this repository.

## Python artifact generation

```bash
python python/generate_pydantic_models.py
```

By default, generated output is written to `/tmp/timeflowerdata-artifacts/timeline_models.py`.

## Private-first Python packaging

This repository can produce a wheel (`.whl`) that other Python projects can install.

### One-time prerequisites

```bash
python -m pip install --upgrade pip
python -m pip install build datamodel-code-generator
```

### Build package locally (same host)

From repository root:

```bash
python python/generate_pydantic_models.py \
	--schema timelineschema.json \
	--output python/src/timeflowerdata_schema/timeline_models.py

python -m build
```

Build output will be in `dist/`.

### Consume from another local project

In the consumer project virtual environment:

```bash
python -m pip install /absolute/path/to/timeflowerdata/dist/timeflowerdata_schema-0.1.0-py3-none-any.whl
```

Then import models in code:

```python
from timeflowerdata_schema import *
```

## Manual GitHub Action release task

Workflow name: `release_schema`

- Trigger mode: manual only (`workflow_dispatch`)
- Not automatically triggered by push or PR
- Required input: `version` (example: `0.1.0`)
- Output 1: `dist/*` uploaded as a workflow artifact named `release_schema_dist_<version>`
- Output 2: GitHub Release with tag `v<version>` and uploaded `*.whl` and `*.tar.gz` assets

Use this when you want an ad-hoc package build and private release distribution.

## Consume from private GitHub Release URL

In a consumer project `requirements.txt`, pin to a specific wheel version from a release asset:

```text
timeflowerdata-schema @ https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/OWNER/REPO/releases/download/v0.1.0/timeflowerdata_schema-0.1.0-py3-none-any.whl
```

Then install:

```bash
python -m pip install -r requirements.txt
```

Notes:

- Keep `v0.1.0` and `0.1.0` aligned to the same released version.
- Use environment variables for `GITHUB_USER` and `GITHUB_TOKEN` (do not hardcode tokens).
- To upgrade, publish a new release (for example `v0.1.1`), update the requirements entry, and reinstall.

## Later: private remote distribution options

When you want to share across hosts, keep it private by publishing to a private package index, for example:

- GitHub Packages (private)
- Azure Artifacts
- Artifactory
- Nexus

Consumer projects then install from that private index using authenticated `pip` settings.

## GitHub Actions snapshot options

Current workflow uploads generated artifacts as workflow artifacts on each push/PR.
Other options you can use later include:

- Publish versioned artifacts as GitHub release assets
- Publish Python package artifacts to a private PyPI-compatible index or PyPI
