# timeflowerdata

Language-agnostic schema repository for timeflower timeline data.

## Repository contents

- `timelineschema.json` — source JSON Schema
- `python/generate_pydantic_models.py` — build script that generates Python (Pydantic) artifacts from the schema

Generated artifacts are intentionally not stored in this repository.

## Python artifact generation

```bash
python python/generate_pydantic_models.py
```

By default, generated output is written to `/tmp/timeflowerdata-artifacts/timeline_models.py`.

## GitHub Actions snapshot options

Current workflow uploads generated artifacts as workflow artifacts on each push/PR.
Other options you can use later include:

- Publish versioned artifacts as GitHub release assets
- Publish Python package artifacts to GitHub Packages or PyPI
