#!/usr/bin/env python3
"""Detect project stack from manifest and source files."""
import json
import os
import sys
from pathlib import Path

def detect(root: str) -> dict:
    root_path = Path(root)
    result = {
        "language": "unknown",
        "framework": "unknown",
        "dependencies": [],
        "source_files": 0,
        "entry_point": None,
    }

    req = root_path / "requirements.txt"
    pkg = root_path / "package.json"
    src_pkg = root_path / "src" / "package.json"

    if req.exists():
        result["language"] = "Python"
        lines = req.read_text(encoding="utf-8").strip().splitlines()
        result["dependencies"] = [l.split("==")[0] for l in lines if l.strip()]
        if any("flask" in d.lower() for d in result["dependencies"]):
            result["framework"] = "Flask"
        if (root_path / "app.py").exists():
            result["entry_point"] = "app.py"

    for p in [pkg, src_pkg]:
        if p.exists():
            result["language"] = "JavaScript"
            data = json.loads(p.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            result["dependencies"] = list(deps.keys())
            if "express" in deps:
                result["framework"] = "Express"
            result["entry_point"] = data.get("main", "src/app.js")

    exclude = {"node_modules", "__pycache__", ".git", ".gemini"}
    for path in root_path.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".js"}:
            if not any(part in exclude for part in path.parts):
                result["source_files"] += 1

    return result

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    info = detect(root)
    print(f"Language:   {info['language']}")
    print(f"Framework:  {info['framework']}")
    print(f"Deps:       {', '.join(info['dependencies'][:5])}")
    print(f"Sources:    {info['source_files']} files")
    print(f"Entry:      {info['entry_point']}")
