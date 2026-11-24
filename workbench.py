#!/usr/bin/env python3
"""Convenience entrypoint; implementation is bundled with the portable AI skill."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'skills/ai-workbench/scripts/workbench.py'),run_name='__main__')
