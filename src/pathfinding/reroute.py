from src.pathfinding.astar import astar
from src.utils.utils import haversine_km


def _is_blocked_by_checker(lat, lon, obstacle_checker, threshold_km=1.0):
    """
    Supports two kinds of obstacle_checkers:
      1. Returns bool → True if blocked.
      2. Returns iterable of (olat, olon) → obstacles near the query point.
    
    If the checker returns a list of obstacle coordinates, we compute 
    haversine distance and treat the point as blocked if within threshold_km.
    """
    res = obstacle_checker(lat, lon)

    # Case 1: checker returns boolean
    if isinstance(res, bool):
        return res

    # Case 2: checker returns list of obstacle coordinates
    try:
        for (olat, olon) in res:
            if haversine_km(lat, lon, olat, olon) <= threshold_km:
                return True
    except Exception:
        # If unexpected format → treat as not blocked
        return False

    return False


def is_path_blocked(path, obstacle_checker, threshold_km=1.0):
    """Checks whether any node on the path is blocked by an obstacle."""
    for node in path:
        if _is_blocked_by_checker(node["lat"], node["lon"], 
                                  obstacle_checker, threshold_km):
            return True
    return False


def reroute(start_id, goal_id, nodes, adj, obstacle_checker, threshold_km=1.0):
    """
    Computes A* path. If path is blocked by obstacles, automatically reroutes.
    Returns:
      (path_ids, distance_km, status_message)
    """
    # Initial A* route
    path, dist = astar(start_id, goal_id, nodes, adj)
    if path is None:
        return None, float("inf"), "No route found"

    # Convert node_ids → coordinate dicts
    path_coords = [
        {"lat": nodes[n]["lat"], "lon": nodes[n]["lon"], "id": n}
        for n in path
    ]

    # If no obstacle → return normal result
    if not is_path_blocked(path_coords, obstacle_checker, threshold_km):
        return path, dist, "OK"

    # Else: remove blocked nodes from adjacency
    modified_adj = _remove_obstacle_nodes(adj, path_coords, 
                                          obstacle_checker, threshold_km)

    # Re-run A*
    new_path, new_dist = astar(start_id, goal_id, nodes, modified_adj)

    if new_path is None:
        return None, float("inf"), "Reroute failed"

    return new_path, new_dist, "REROUTED"


def _remove_obstacle_nodes(adj, path_nodes, 
                           obstacle_checker, threshold_km=1.0):
    """Produce a modified adjacency dict with blocked nodes removed."""
    blocked_ids = []

    # Find nodes that intersect or fall within obstacle threshold
    for p in path_nodes:
        if _is_blocked_by_checker(p["lat"], p["lon"], 
                                  obstacle_checker, threshold_km):
            blocked_ids.append(p["id"])

    # Build modified adjacency without those nodes
    new_adj = {}
    for node, neighbors in adj.items():
        if node in blocked_ids:
            continue
        new_adj[node] = [
            (n, d) for n, d in neighbors if n not in blocked_ids
        ]

    return new_adj
