from src.graph_builder.build_graph import generate_coarse_grid
from src.pathfinding.reroute import reroute
from src.graph_builder.config import COARSE_RES


def fake_obstacle_checker(lat, lon):
    # Block only a narrow band (NOT the whole row)
    return 10.027 < lat < 10.033


def test_reroute():
    lat_min, lat_max = 10.0, 10.1
    lon_min, lon_max = 70.0, 70.1

    nodes_dict, adj = generate_coarse_grid(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        res=COARSE_RES,
        land_mask=None
    )

    nodes = {v["id"]: v for v in nodes_dict.values()}

    start = min(nodes.keys())
    goal = max(nodes.keys())

    path, dist, status = reroute(start, goal, nodes, 
                                 adj, fake_obstacle_checker)

    assert status in ("OK", "REROUTED")
    assert path is not None
    assert dist > 0

    print("\n✔ Reroute test passed")
