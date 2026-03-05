#!/usr/bin/env python3
from pathlib import Path
import runpy

if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "custom_tools" / "external_tools" / "download_datasheets.py"
    runpy.run_path(str(target), run_name="__main__")
