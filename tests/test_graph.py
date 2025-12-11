from src.graph_builder.build_graph import generate_coarse_grid
from src.graph_builder.config import COARSE_RES
from src.utils.utils import haversine_km


def test_small_coarse_grid():
    """
    Test that a small coarse grid area:
    - generates nodes correctly
    - contains adjacency links
    - produces valid haversine distances
    """

    # Very small area for fast test
    lat_min, lat_max = 10.0, 10.2
    lon_min, lon_max = 70.0, 70.2

    nodes, adj = generate_coarse_grid(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        res=COARSE_RES,
        land_mask=None
    )

    # ✔ 1. nodes exist
    assert len(nodes) > 0, "No nodes generated in coarse grid."

    # ✔ 2. adjacency exists
    assert len(adj) > 0, "Adjacency structure is empty."

    # ✔ 3. neighbor distance sanity check
    first_node = list(adj.keys())[0]
    neighbors = adj[first_node]

    assert len(neighbors) > 0, "Sample node has no neighbors!"

    neighbor_id, dist_km = neighbors[0]

    assert dist_km > 0, "Distance must be positive."
    assert dist_km < 20, f"Distance too large for coarse grid: {dist_km}"

    print("\n✔ test_small_coarse_grid passed successfully!")