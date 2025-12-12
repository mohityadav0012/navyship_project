import matplotlib
matplotlib.use("Agg")   # <-- Correct place

import matplotlib.pyplot as plt
import os
  


def visualize_route(
    nodes,
    path,
    obstacles=None,
    show_nodes=True,
    save_path=None,
    figsize=(10, 8)
):
    """
    Styled visualization of the ocean route.

    Parameters
    ----------
    nodes : dict
        Node dictionary {id: {"lat":..., "lon":...}}
    path : list
        Ordered list of node_ids representing the route
    obstacles : list of (lat, lon), optional
        Points to mark as obstacles
    show_nodes : bool
        Whether to plot all graph nodes faintly
    save_path : str
        File path to save the figure (PNG)
    figsize : tuple
        Size of the plot

    Returns
    -------
    fig : matplotlib Figure
    """

    # Extract path coordinates
    path_lats = [nodes[n]["lat"] for n in path]
    path_lons = [nodes[n]["lon"] for n in path]

    # Extract all node coordinates
    all_lats = [v["lat"] for v in nodes.values()]
    all_lons = [v["lon"] for v in nodes.values()]

    fig, ax = plt.subplots(figsize=figsize)

    # === Ocean background ===
    ax.set_facecolor("#ADD8E6")  # light ocean blue

    # === Plot grid nodes (faint) ===
    if show_nodes:
        ax.scatter(
            all_lons, all_lats,
            s=5,
            c="#ffffff",
            alpha=0.15,
            label="Grid nodes"
        )

    # === Plot path ===
    ax.plot(
        path_lons, path_lats,
        linewidth=3,
        color="#ffcc00",
        label="Ship route"
    )

    # === Start and End markers ===
    ax.scatter(
        path_lons[0], path_lats[0],
        c="green", s=80, label="Start"
    )
    ax.scatter(
        path_lons[-1], path_lats[-1],
        c="red", s=80, label="Destination"
    )

    # === Plot obstacles ===
    if obstacles:
        obs_lons = [ob[1] for ob in obstacles]
        obs_lats = [ob[0] for ob in obstacles]
        ax.scatter(
            obs_lons, obs_lats,
            c="black", s=40,
            marker="x",
            label="Obstacles"
        )

    # === Styling ===
    ax.set_title("Ocean Navigation Route", fontsize=16)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(color="white", linestyle="--", linewidth=0.5, alpha=0.3)
    ax.legend()

    # Save figure if requested
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300)
        print(f"Plot saved to {save_path}")

    return fig
