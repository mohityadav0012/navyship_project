# scripts/test_navigator.py

import os
import sys

# Ensure project root is in sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from src.core_engine.navigator import Navigator

nav = Navigator()

nav.navigate(
    start_lat=10.0,
    start_lon=70.0,
    end_lat=12.0,
    end_lon=75.0,
    verbose=True
)
