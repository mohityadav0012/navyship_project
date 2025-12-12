# tests/test_core_engine.py

from src.core_engine.get_path import get_shortest_path
from src.core_engine.check_obstacles import is_obstacle


def test_get_shortest_path():
    result = get_shortest_path(10.0, 70.0, 10.5, 70.5)

    assert result["status"] == "OK"
    assert isinstance(result["distance_km"], float)
    assert len(result["path_latlon"]) > 0


def test_check_obstacles():
    # Dummy ML model + no restricted zones = always safe for now
    assert is_obstacle(10.0, 70.0) is False
