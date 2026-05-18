#!/usr/bin/env python3
"""Generate Pydantic models from the repository JSON Schema."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def _default_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "timelineschema.json"


def _default_output_path() -> Path:
    return Path("/tmp/timeflowerdata-artifacts/timeline_models.py")


def _ensure_non_empty_schema(schema_path: Path) -> Path:
    content = schema_path.read_text(encoding="utf-8").strip()
    if content:
        json.loads(content)
        return schema_path

    temp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    with temp_file:
        temp_file.write("{}")
    return Path(temp_file.name)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Pydantic models from timelineschema.json."
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=_default_schema_path(),
        help="Path to input JSON Schema file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=_default_output_path(),
        help="Path to generated Python file.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    schema_path = args.schema.resolve()
    output_path = args.output.resolve()

    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 1

    if importlib.util.find_spec("datamodel_code_generator") is None:
        print(
            "Missing dependency: datamodel-code-generator. "
            "Install with `pip install datamodel-code-generator`.",
            file=sys.stderr,
        )
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    input_path = _ensure_non_empty_schema(schema_path)
    temp_input = input_path != schema_path

    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input",
        str(input_path),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_path),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--disable-timestamp",
        "--use-annotated",
    ]
    try:
        subprocess.run(cmd, check=True)
    finally:
        if temp_input:
            input_path.unlink(missing_ok=True)
    print(f"Generated Pydantic models: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
