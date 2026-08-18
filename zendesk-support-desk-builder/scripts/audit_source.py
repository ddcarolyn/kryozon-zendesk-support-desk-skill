#!/usr/bin/env python3
"""Create a deterministic, content-free manifest of a support desk source tree."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


INCLUDE_SUFFIXES = {".js", ".jsx", ".mjs", ".ts", ".tsx", ".css", ".sql", ".md", ".json", ".yaml", ".yml"}
EXCLUDED_PARTS = {".artifact-build", ".git", ".wrangler", "node_modules", "dist", "build", "data", "secrets"}
EXCLUDED_NAMES = {".env", "support.db", "token.json"}
SENSITIVE_NAME_PARTS = ("client_secret", "credential", "token", ".env")


def allowed(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    lowered = path.name.lower()
    if lowered in EXCLUDED_NAMES or any(part in lowered for part in SENSITIVE_NAME_PARTS):
        return False
    return path.suffix.lower() in INCLUDE_SUFFIXES


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: audit_source.py <support-desk-project>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"Project directory not found: {root}", file=sys.stderr)
        return 2

    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and allowed(path, root):
            stat = path.stat()
            files.append({
                "path": path.relative_to(root).as_posix(),
                "size": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "sha256": digest(path),
            })

    output = {
        "project_name": root.name,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "files": files,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
