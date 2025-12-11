from src.graph_builder.build_graph import generate_coarse_grid
from src.pathfinding.dijkstra import dijkstra
from src.graph_builder.config import COARSE_RES


def test_dijkstra_simple():
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

    start = list(nodes_dict.values())[0]["id"]
    goal = list(nodes_dict.values())[-1]["id"]

    path, dist = dijkstra(start, goal, adj)

    assert path is not None
    assert dist > 0

    print("\n✔ Dijkstra test passed")
