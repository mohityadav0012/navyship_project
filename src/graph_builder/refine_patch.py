from collections import defaultdict
from src.utils.utils import haversine_km
from .config import FINE_RES
try:
    from shapely.geometry import Point
except Exception:
    Point = None

"""
This file generates a fine-resolution local patch of the navigation graph 
for high-detail routing inside a smaller bounding box.
"""


def generate_patch(lat_min, lat_max, lon_min, 
                   lon_max, res=FINE_RES, land_mask=None):
    """Create a fine-resolution patch in bbox. 
    Returns nodes (dict) and adj (dict)."""
    n_lat = int(round((lat_max - lat_min) / res)) + 1
    n_lon = int(round((lon_max - lon_min) / res)) + 1

    nodes = {}
    node_id = 0
    for i in range(n_lat):
        lat = lat_min + i * res
        for j in range(n_lon):
            lon = lon_min + j * res
            if land_mask is not None and Point is not None:
                if Point(lon, lat).within(land_mask):
                    continue
            key = f"r_{i}_{j}"
            nodes[key] = {"id": node_id, 
                          "i": i, "j": j, "lat": lat, "lon": lon}
            node_id += 1

    # neighbor offsets (8-neigh)
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), 
               (-1, -1), (-1, 1), (1, -1), (1, 1)]
    # mapping from (i,j) to key
    ij_to_key = {(v["i"], v["j"]): k for k, v in nodes.items()}

    adj = defaultdict(list)
    for k,  v in nodes.items():
        i, j = v["i"], v["j"]
        for di, dj in offsets:
            ni, nj = i+di, j+dj
            nk = ij_to_key.get((ni, nj))
            if nk:
                dist = haversine_km(v["lat"], v["lon"], 
                                    nodes[nk]["lat"], nodes[nk]["lon"])
                adj[v["id"]].append((nodes[nk]["id"], dist))

    return nodes, dict(adj)

