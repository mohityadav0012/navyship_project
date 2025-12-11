'''
basically here i am describing the sizes and all for grids.
'''

from pathlib import Path

LAT_MIN=-40.0 #south
LAT_MAX=30.0 #north
LON_MAX=120.0 #east
LON_MIN=20.0 #west
LAND_MASK_PATH = None


COARSE_RES = 0.05    # ~5.5 km - base global grid 
FINE_RES = 0.01      # ~1.1 km - high resolution patches

NEIGHBOR_OFFSETS = [
    (-1,  0), (1,  0), (0, -1), (0,  1),
    (-1, -1), (-1, 1), (1, -1), (1,  1)
]

OUTPUT_DIR=Path("data/graph")
NODES_FILE=OUTPUT_DIR/"nodes_coarse.json"
PICKLE_FILE=OUTPUT_DIR/"graph_coarse.pkl"

