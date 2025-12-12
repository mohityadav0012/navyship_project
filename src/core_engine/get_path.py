from src.graph_builder.ocean_grid import load_nodes, load_graph_pickle
from src.pathfinding.utils import find_nearest_node, nodes_to_coordinates
from src.pathfinding.astar import astar


def get_shortest_path(start_lat, start_lon, goal_lat, goal_lon):
    """
    Compute shortest path using A* without obstacle rerouting.
    Clean and simple function used by the API/backend.
    """

    # Load graph data
    nodes = load_nodes()
    adj = load_graph_pickle()

    if not nodes or not adj:
        raise RuntimeError("Graph data missing. Please generate graph first.")

    # Map coordinates -> nearest nodes
    start_id, _ = find_nearest_node(start_lat, start_lon, nodes)
    goal_id, _ = find_nearest_node(goal_lat, goal_lon, nodes)

    # Run A* algorithm
    path_ids, distance_km = astar(start_id, goal_id, nodes, adj)

    if path_ids is None:
        return {
            "status": "NO_PATH",
            "distance_km": None,
            "path_latlon": [],
            "path_node_ids": [],
        }

    # Convert to coordinates
    path_coords = nodes_to_coordinates(path_ids, nodes)

    return {
        "status": "OK",
        "distance_km": distance_km,
        "path_latlon": path_coords,
        "path_node_ids": path_ids,
    }


if __name__ == "__main__":
    # Quick check
    result = get_shortest_path(10.0, 70.0, 12.0, 75.0)
    print(result)
