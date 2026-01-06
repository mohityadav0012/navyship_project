import numpy as np
import heapq
from scipy.ndimage import distance_transform_edt

def create_environment_from_data(width, height, land_grid, hazard_grid, current_u_grid, current_v_grid):
    # land_grid is expected to be 0 for water, 1 for land
    land_map = np.array(land_grid)
    hazard_map = np.array(hazard_grid) if hazard_grid else np.zeros((height, width))
    
    # Calculate distance to nearest land
    dist_to_land = distance_transform_edt(1 - land_map)

    # Currents
    currents = np.stack((current_u_grid, current_v_grid), axis=-1)

    return land_map, hazard_map, dist_to_land, currents

def haversine_heuristic(a, b):
    # Simple Euclidean distance for grid
    r1, c1 = a
    r2, c2 = b
    return np.sqrt((r1-r2)**2 + (c1-c2)**2)

def get_neighbors(node, shape):
    r, c = node
    h, w = shape
    steps = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    valid = []
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            valid.append((nr, nc))
    return valid

def calculate_cost(current, neighbor, mode, env_data):
    land, hazard, dist_land, currents = env_data

    # Strict check for land
    if land[neighbor] == 1: 
        return float('inf')

    base_dist = np.linalg.norm(np.array(current) - np.array(neighbor))

    # Base Hazard Penalty
    hazard_penalty = 0
    if hazard[neighbor] == 1:
        hazard_penalty = 50.0 # High cost but traversable if necessary? Or make it untraversable?
        # User said "bad weather" so probably just very costly/dangerous.
        # Let's make it very high.
    
    if mode == 'fastest':
        cur_vec = currents[current]
        move_vec = np.array(neighbor) - np.array(current)
        move_vec = move_vec / (np.linalg.norm(move_vec) + 1e-5)
        
        # Dot product: positive if current helps, negative if opposes
        assist = np.dot(cur_vec, move_vec)

        # Speed logic
        speed = 1.0 + (assist * 0.5)
        
        return (base_dist / max(0.1, speed)) + hazard_penalty

    elif mode == 'fuel_efficient':
        cur_vec = currents[current]
        move_vec = np.array(neighbor) - np.array(current)
        move_vec = move_vec / (np.linalg.norm(move_vec) + 1e-5)
        
        # Resistance: opposing current increases cost
        resistance = -np.dot(cur_vec, move_vec)

        return base_dist * (1 + max(0, resistance) * 3) + hazard_penalty

    elif mode == 'coastal':
        dist = dist_land[neighbor]
        penalty = 0
        if dist > 8: penalty = dist * 2
        if dist < 2: penalty = 20
        return base_dist + penalty + hazard_penalty

    return base_dist

def run_astar(start, end, width, height, land_grid, hazard_grid, current_u, current_v, mode):
    # Prepare env data
    try:
        env_data = create_environment_from_data(width, height, land_grid, hazard_grid, current_u, current_v)
        land = env_data[0]
        
        start = tuple(start)
        end = tuple(end)

        if land[start] or land[end]:
            return None

        pq = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while pq:
            _, current = heapq.heappop(pq)

            if current == end: break

            for next_node in get_neighbors(current, land.shape):
                new_cost = cost_so_far[current] + calculate_cost(current, next_node, mode, env_data)

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + haversine_heuristic(next_node, end)
                    heapq.heappush(pq, (priority, next_node))
                    came_from[next_node] = current

        if end not in came_from:
            return None
        
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = came_from[curr]
        return path[::-1] # Reverse list
    except Exception as e:
        print(f"Error in astar: {e}")
        return None
