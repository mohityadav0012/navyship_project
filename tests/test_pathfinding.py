from src.graph_builder.refine_patch import generate_patch
from src.graph_builder.config import FINE_RES


def test_fine_patch():
    """
    Test that a fine-resolution patch:
    - generates small grid correctly
    - builds adjacency properly
    - produces realistic short distances
    """

    lat_min, lat_max = 10.0, 10.01
    lon_min, lon_max = 70.0, 70.01

    nodes, adj = generate_patch(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        res=FINE_RES,
        land_mask=None
    )

    # ✔ 1. nodes exist
    assert len(nodes) > 0, "Fine patch returned no nodes!"

    # ✔ 2. adjacency exists
    assert len(adj) > 0, "Fine patch adjacency is empty!"

    # ✔ 3. pick a sample and check distance
    first_node = list(adj.keys())[0]
    neighbors = adj[first_node]

    assert len(neighbors) > 0, "Fine patch node has no neighbors!"

    neighbor_id, dist_km = neighbors[0]

    assert dist_km > 0, "Fine-grid distance must be > 0"
    assert dist_km < 5, f"Distance too large for fine resolution: {dist_km}"

    print("\n✔ test_fine_patch passed successfully!")