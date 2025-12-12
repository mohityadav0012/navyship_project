import sys
from pathlib import Path
from src.graph_builder.ocean_grid import load_nodes, load_graph_pickle
from src.pathfinding.utils import find_nearest_node, nodes_to_coordinates
from src.pathfinding.reroute import reroute
from src.obstacle_detection.obstacle_engine import ObstacleEngine

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


def simulate_route(start_lat, start_lon, goal_lat, goal_lon):
    """
    Full navigation pipeline:
      1. Load graph
      2. Convert coordinates → nearest nodes
      3. Run reroute-aware A* pathfinding
      4. Apply rule-based + ML obstacle detection
      5. Return path, distance, status
    """

    print("\n===== NAVIGATION SIMULATION STARTED =====")

    # Load nodes + adjacency
    nodes = load_nodes()
    adj = load_graph_pickle()

    if not nodes or not adj:
        raise RuntimeError("Graph data missing. Generate graph first.")

    # Map lat/lon → nearest nodes
    start_id, start_dist = find_nearest_node(start_lat, start_lon, nodes)
    goal_id, goal_dist = find_nearest_node(goal_lat, goal_lon, nodes)

    print(f"Start input     : ({start_lat}, {start_lon})")
    print(f"Nearest node    : {start_id} (distance {start_dist:.3f} km)")
    print(f"Goal input      : ({goal_lat}, {goal_lon})")
    print(f"Nearest node    : {goal_id} (distance {goal_dist:.3f} km)")

    # Obstacle engine (rule-based + ML)
    engine = ObstacleEngine()

    # Compute safe path
    path_ids, dist_km, status = reroute(
        start_id, goal_id, nodes, adj, engine.obstacle_checker
    )

    # Convert node IDs -> coordinates for readability
    path_coords = nodes_to_coordinates(path_ids, nodes) if path_ids else []

    print("\n===== RESULTS =====")
    print(f"Status       : {status}")
    print(f"Distance     : {dist_km:.2f} km")
    print(f"Path length  : {len(path_ids) if path_ids else 0} nodes")

    if path_coords:
        print("\n--- First 5 path coordinates ---")
        for lat, lon in path_coords[:5]:
            print(f"({lat:.5f}, {lon:.5f})")
        if len(path_coords) > 5:
            print(f"... {len(path_coords)-5} more")

    print("\n===== NAVIGATION COMPLETE =====\n")

    return path_ids, path_coords, dist_km, status


# Direct testing
if __name__ == "__main__":
    simulate_route(start_lat=10.0, start_lon=70.0, 
                   goal_lat=12.0, goal_lon=75.0)
