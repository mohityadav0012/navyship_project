# scripts/test_visualize.py

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

# noqa: E402
from src.graph_builder.ocean_grid import load_nodes, load_graph_pickle
from src.pathfinding.dijkstra import dijkstra
from src.core_engine.visualize_route import visualize_route

nodes = load_nodes()
adj = load_graph_pickle()

start = min(nodes.keys())
goal = max(nodes.keys())

path, dist = dijkstra(start, goal, adj)

visualize_route(nodes, path, save_path="data/plots/test_route.png")
