from shapely.geometry import Polygon
from src.obstacle_detection.obstacle_engine import ObstacleEngine


def test_rule_based_land_mask():
    # square polygon that covers (10, 20)
    poly = Polygon([(20, 10), (21, 10), (21, 11), (20, 11)])
    engine = ObstacleEngine(land_mask=poly)

    assert engine.obstacle_checker(10.5, 20.5) is True
    assert engine.obstacle_checker(12.0, 25.0) is False


def test_rule_based_restricted_zone():
    poly = Polygon([(70, 10), (71, 10), (71, 11), (70, 11)])
    engine = ObstacleEngine(restricted_polygons=[poly])

    assert engine.obstacle_checker(10.5, 70.5) is True
    assert engine.obstacle_checker(15.0, 75.0) is False


def test_ml_checker_stub():
    # Mock ML checker always returns True
    def fake_ml(lat, lon):
        return True

    engine = ObstacleEngine(ml_checker=fake_ml)

    assert engine.obstacle_checker(10, 20) is True
