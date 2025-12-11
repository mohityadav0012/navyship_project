import pickle
import json
from pathlib import Path
from .config import NODES_FILE, PICKLE_FILE


def load_nodes(path=NODES_FILE):
    path = Path(path)
    with open(path, "r") as f:
        data = json.load(f)
    # return as dict id -> (lat, lon)
    return {d["id"]: {"lat": d["lat"], "lon": d["lon"], "i": d.get("i"), "j": d.get("j")} for d in data}

def load_graph_pickle(path=PICKLE_FILE):
    path = Path(path)
    with open(path, "rb") as f:
        adj = pickle.load(f)
    return adj