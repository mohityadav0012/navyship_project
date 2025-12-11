import heapq
from math import inf


def dijkstra(start_id, goal_id, adj):
    """
    Basic Dijkstra's algorithm.
    Works without latitude/longitude — uses only adjacency distances.
    Returns (path, total_cost_km).
    """

    pq = [(0, start_id)]   # (distance_from_start, node_id)
    dist = {start_id: 0}
    came_from = {}

    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current == goal_id:
            return reconstruct_path(came_from, current), current_dist

        if current in visited:
            continue
        visited.add(current)

        for neighbor, edge_cost in adj.get(current, []):
            new_cost = current_dist + edge_cost
            if new_cost < dist.get(neighbor, inf):
                dist[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None, inf


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]
