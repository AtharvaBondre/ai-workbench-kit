#!/usr/bin/env python3
"""Same command entry point when the skill is installed on its own."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'scripts/workbench.py'),run_name='__main__')
