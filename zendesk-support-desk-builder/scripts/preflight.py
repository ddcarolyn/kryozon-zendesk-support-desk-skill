#!/usr/bin/env python3
"""Check prerequisites without reading or printing credential values."""

from __future__ import annotations

import os
import shutil
import sys


TOOLS = ("git", "node", "npm", "python3")
LOCAL_VARS = (
    "GOOGLE_OAUTH_JSON",
    "SHOPIFY_STORE_DOMAIN",
    "SHOPIFY_CLIENT_ID",
    "SHOPIFY_CLIENT_SECRET",
    "DEEPSEEK_API_KEY",
)


def main() -> int:
    missing_tools = [name for name in TOOLS if shutil.which(name) is None]
    present_vars = [name for name in LOCAL_VARS if os.environ.get(name)]
    missing_vars = [name for name in LOCAL_VARS if not os.environ.get(name)]

    print("Zendesk support desk preflight")
    print("Tools:")
    for name in TOOLS:
        print(f"  {'OK' if name not in missing_tools else 'MISSING'}  {name}")
    print("Environment variable names (values are never read or printed):")
    for name in present_vars:
        print(f"  SET      {name}")
    for name in missing_vars:
        print(f"  NOT SET  {name}")

    if missing_tools:
        print("Result: install the missing tools before scaffolding.")
        return 1
    print("Result: base tools are ready. Configure missing variables locally when their integrations are enabled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
