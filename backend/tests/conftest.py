import os
import sys
from pathlib import Path

# make `app`, `ml`, `simulator` importable no matter where pytest is started
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("LLM_PROVIDER", "mock")
os.environ.setdefault("DEMO_MODE", "true")
