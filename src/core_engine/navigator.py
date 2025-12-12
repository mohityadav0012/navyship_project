# src/core_engine/navigator.py

import time
from src.graph_builder.ocean_grid import load_nodes, load_graph_pickle
from src.pathfinding.utils import find_nearest_node, nodes_to_coordinates
from src.pathfinding.reroute import reroute
from src.obstacle_detection.obstacle_engine import ObstacleEngine


class Navigator:
    """
    Dynamic ship navigation engine.
    Continuously tracks the ship's position and reroutes if obstacles appear.
    """

    def __init__(self, reroute_threshold_km=1.5, sleep_interval=0.5):
        self.nodes = load_nodes()
        self.adj = load_graph_pickle()
        self.obstacle_engine = ObstacleEngine()
        self.threshold_km = reroute_threshold_km
        self.sleep = sleep_interval

    # ---------------------------------------------------------
    def compute_initial_route(self, start_lat, start_lon, end_lat, end_lon):
        """Compute the initial route using reroute()."""

        start_id, _ = find_nearest_node(start_lat, start_lon, self.nodes)
        goal_id, _ = find_nearest_node(end_lat, end_lon, self.nodes)

        path, dist, status = reroute(
            start_id,
            goal_id,
            self.nodes,
            self.adj,
            obstacle_checker=self.obstacle_engine.is_obstacle,   # FIXED
            threshold_km=self.threshold_km
        )

        return start_id, goal_id, path, dist, status

    # ---------------------------------------------------------
    def navigate(self, start_lat, start_lon, end_lat, end_lon, verbose=True):
        """Main dynamic navigation loop."""

        start_id, goal_id, path, dist, status = self.compute_initial_route(
            start_lat, start_lon, end_lat, end_lon
        )

        if path is None:
            print("❌ No initial route found!")
            return None

        if verbose:
            print("\n===== DYNAMIC NAVIGATION STARTED =====")
            print(f"Initial route status: {status}, distance: {dist:.2f} km")

        current_path = path
        current_index = 0

        while current_index < len(current_path):

            node_id = current_path[current_index]
            lat = self.nodes[node_id]["lat"]
            lon = self.nodes[node_id]["lon"]

            # ---------------------------------------------------------
            # Obstacle check at this node
            # ---------------------------------------------------------
            if self.obstacle_engine.is_obstacle(lat, lon):      # FIXED
                if verbose:
                    print(f"\n⚠️  Obstacle detected at index {current_index}, re-routing...")

                new_path, new_dist, new_status = reroute(
                    node_id,
                    goal_id,
                    self.nodes,
                    self.adj,
                    obstacle_checker=self.obstacle_engine.is_obstacle,  # FIXED
                    threshold_km=self.threshold_km
                )

                if new_path is None:
                    print("❌ Reroute failed. Stopping navigation.")
                    return None

                current_path = new_path
                current_index = 0

                if verbose:
                    print(f"✅ Rerouted: {new_status}, new distance: {new_dist:.2f} km")

                continue

            # ---------------------------------------------------------
            # Normal movement
            # ---------------------------------------------------------
            if verbose:
                print(f"→ Moving to node {node_id}: ({lat:.4f}, {lon:.4f})")

            current_index += 1
            time.sleep(self.sleep)

        if verbose:
            print("\n===== DESTINATION REACHED SUCCESSFULLY =====")

        return nodes_to_coordinates(current_path, self.nodes)
