from src.graph_builder.build_graph import generate_coarse_grid
from src.pathfinding.astar import astar
from src.graph_builder.config import COARSE_RES


def test_astar_simple():
    # Tiny bbox
    lat_min, lat_max = 10.0, 10.05
    lon_min, lon_max = 70.0, 70.05

    nodes_dict, adj = generate_coarse_grid(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        res=COARSE_RES,
        land_mask=None
    )

    # Convert nodes dict for A*
    nodes = {v["id"]: {"lat": v["lat"], "lon": v["lon"]} 
             for v in nodes_dict.values()}

    start = min(nodes.keys())
    goal = max(nodes.keys())

    path, dist = astar(start, goal, nodes, adj)

    assert path is not None
    assert dist > 0
    assert len(path) > 1

    print("\n✔ A* test passed")
