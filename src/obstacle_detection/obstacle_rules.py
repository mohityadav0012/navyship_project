from shapely.geometry import Point


class ObstacleRules:
    def __init__(self, land_mask=None, restricted_polygons=None):
        self.land_mask = land_mask
        self.restricted_polygons = restricted_polygons or []

    def is_land(self, lat, lon):
        if self.land_mask is None:
            return False
        return Point(lon, lat).within(self.land_mask)

    def is_restricted_zone(self, lat, lon):
        p = Point(lon, lat)
        return any(p.within(poly) for poly in self.restricted_polygons)

    def rule_based_checker(self, lat, lon):
        """
        Returns True if location is forbidden based on static rules.
        """
        if self.is_land(lat, lon):
            return True
        if self.is_restricted_zone(lat, lon):
            return True
        return False
