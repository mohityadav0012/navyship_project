
import heapq
from math import inf
from src.utils.utils import haversine_km


def astar(start_id, goal_id, nodes, adj):
    """
    A* pathfinding on the ocean navigation graph.
    Returns (path, total_cost_km).
    
    nodes: {id: {"lat": ..., "lon": ...}}
    adj:   {id: [(neighbor_id, distance_km), ...]}
    """

    # Min-heap priority queue: (estimated_total_cost, node_id)
    open_set = [(0, start_id)]

    came_from = {}
    g_score = {start_id: 0}

    # f(n) = g(n) + h(n)
    f_score = {
        start_id: haversine_km(
            nodes[start_id]["lat"], nodes[start_id]["lon"],
            nodes[goal_id]["lat"], nodes[goal_id]["lon"]
        )
    }

    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        # Goal reached
        if current == goal_id:
            return reconstruct_path(came_from, current), g_score[current]

        if current in visited:
            continue
        visited.add(current)

        for neighbor, dist in adj.get(current, []):
            tentative_g = g_score[current] + dist

            if tentative_g < g_score.get(neighbor, inf):
                # Found better path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                heuristic = haversine_km(
                    nodes[neighbor]["lat"], nodes[neighbor]["lon"],
                    nodes[goal_id]["lat"], nodes[goal_id]["lon"],
                )
                f_score[neighbor] = tentative_g + heuristic

                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, inf  # No path found


def reconstruct_path(came_from, current):
    """Backtracks from goal to start."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]
