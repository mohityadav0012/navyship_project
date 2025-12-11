import json
import pickle
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

from src.utils.utils import haversine_km
from .config import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, COARSE_RES, NEIGHBOR_OFFSETS, OUTPUT_DIR, NODES_FILE, PICKLE_FILE, LAND_MASK_PATH

"""
This file generates a coarse ocean-navigation graph by creating grid nodes, 
removing land points, and connecting each water node to its neighboring nodes with haversine distance weights.
"""

try:
    import geopandas as gpd
    from shapely.geometry import Point
    HAS_GEOPANDAS = True
except Exception:
    HAS_GEOPANDAS = False
    Point = None


def estimate_node_counts(lat_min, lat_max, lon_min, lon_max, res):
    n_lat = int(round((lat_max - lat_min) / res)) + 1
    n_lon = int(round((lon_max - lon_min) / res)) + 1
    return n_lat, n_lon, n_lat * n_lon


def load_land_mask(path):
    if not HAS_GEOPANDAS:
        raise RuntimeError("geopandas required for land masking. Install geopandas to use LAND_MASK.")
    gdf = gpd.read_file(path)
    return gdf.unary_union 



def generate_coarse_grid(lat_min=LAT_MIN, lat_max=LAT_MAX, lon_min=LON_MIN, lon_max=LON_MAX, res=COARSE_RES, land_mask=None):
    n_lat = int(round((lat_max - lat_min) / res)) + 1
    n_lon = int(round((lon_max - lon_min) / res)) + 1

    nodes = {}
    node_id = 0

    for i in tqdm(range(n_lat), desc="lat rows"):
        lat = lat_min + i * res
        for j in range(n_lon):
            lon = lon_min + j * res
            # skip if on land (if mask provided)
            if land_mask is not None:
                if Point(lon, lat).within(land_mask):
                    continue
            key = f"{i}_{j}"
            nodes[key] = {"id": node_id, "i": i, "j": j, "lat": lat, "lon": lon}
            node_id += 1

    # Build adjacency as dict: node_id -> list of (neighbor_id, dist_km)
    adj = defaultdict(list)
    id_to_key = {v["id"]: k for k,v in nodes.items()}
    key_to_id = {k: v["id"] for k,v in nodes.items()}

    for key, v in tqdm(nodes.items(), desc="building adjacency"):
        i, j = v["i"], v["j"]
        this_id = v["id"]
        for di, dj in NEIGHBOR_OFFSETS:
            ni, nj = i + di, j + dj
            neighbor_key = f"{ni}_{nj}"
            if neighbor_key in key_to_id:
                neigh_id = key_to_id[neighbor_key]
                lat2, lon2 = nodes[neighbor_key]["lat"], nodes[neighbor_key]["lon"]
                dist = haversine_km(v["lat"], v["lon"], lat2, lon2)
                adj[this_id].append((neigh_id, dist))

    return nodes, dict(adj)


def save_nodes_json(nodes, path=NODES_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [{"id": v["id"], "lat": v["lat"], "lon": v["lon"], "i": v["i"], "j": v["j"]} for v in nodes.values()]
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved {len(data)} nodes to {path}")



def save_graph_pickle(adj, path=PICKLE_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(adj, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Saved adjacency pickle to {path}")




def main_generate_coarse(force=False):
    # estimate size
    n_lat, n_lon, total = estimate_node_counts(LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, COARSE_RES)
    print(f"Estimated grid: {n_lat} x {n_lon} = {total} raw points (before land mask).")

    land_mask = None
    if LAND_MASK_PATH:
        if not HAS_GEOPANDAS:
            raise RuntimeError("LAND_MASK_PATH set but geopandas not installed.")
        land_mask = load_land_mask(LAND_MASK_PATH)
        print("Loaded land mask.")

    nodes, adj = generate_coarse_grid(land_mask=land_mask)
    save_nodes_json(nodes)
    save_graph_pickle(adj)

if __name__ == "__main__":
    main_generate_coarse()