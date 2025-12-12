from src.obstacle_detection.obstacle_rules import ObstacleRules
from src.obstacle_detection.inference import obstacle_checker_ml


class ObstacleEngine:
    """
    Combines rule-based and ML-based obstacle detection.
    Can be plugged directly into the rerouting engine.
    """

    def __init__(self, land_mask=None, restricted_polygons=None, 
                 ml_checker=obstacle_checker_ml):
        self.rules = ObstacleRules(
            land_mask=land_mask,
            restricted_polygons=restricted_polygons
        )
        self.ml_checker = ml_checker

    def obstacle_checker(self, lat, lon):
        """
        Returns True if location is blocked by either:
        - Static rules (land, restricted zones)
        - ML-based detection (icebergs, objects)
        """

        # Rule-based layer ALWAYS wins
        if self.rules.rule_based_checker(lat, lon):
            return True

        # ML detection
        return self.ml_checker(lat, lon)
