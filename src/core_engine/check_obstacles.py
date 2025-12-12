from src.obstacle_detection.obstacle_engine import ObstacleEngine


# Load once globally
_engine = ObstacleEngine()


def is_obstacle(lat, lon):
    """
    Check if a given (lat, lon) point is blocked by:
      - rule-based obstacles (land, restricted areas)
      - ML model-based detection (dummy or real)
    """

    return _engine.obstacle_checker(lat, lon)


def batch_check(coords_list):
    """
    coords_list: list of (lat, lon)
    Returns dict: {index: True/False}
    """

    results = {}
    for idx, (lat, lon) in enumerate(coords_list):
        results[idx] = _engine.obstacle_checker(lat, lon)

    return results


if __name__ == "__main__":
    print(is_obstacle(10.0, 70.0))  # Expected False (dummy model)
