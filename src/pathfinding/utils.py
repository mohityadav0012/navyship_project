# src/pathfinding/utils.py

from src.utils.utils import haversine_km


def find_nearest_node(lat, lon, nodes):
    """
    Given a real latitude and longitude, return the closest node_id
    in the graph.

    nodes: dict {node_id: {"lat":..., "lon":...}}
    """
    nearest = None
    min_dist = float("inf")

    for nid, info in nodes.items():
        d = haversine_km(lat, lon, info["lat"], info["lon"])
        if d < min_dist:
            min_dist = d
            nearest = nid

    return nearest, min_dist


def nodes_to_coordinates(path, nodes):
    """
    Convert a path of node_ids → list of (lat, lon) pairs.
    Useful for frontend visualization and API output.
    """
    if path is None:
        return []

    return [(nodes[n]["lat"], nodes[n]["lon"]) for n in path]


def load_graph(nodes, adj):
    """
    Placeholder for future optimization:
    Could add caching, memory mapping, lazy loading.

    For now just returns (nodes, adj) unchanged.
    """
    return nodes, adj
