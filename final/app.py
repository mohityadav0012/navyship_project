from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logic
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

# Demo Data (Simple hardcoded examples)
DEMOS = {
    "1": {
        "name": "Strait Passage",
        "width": 60,
        "height": 60,
        "landGrid": [[0]*60 for _ in range(60)], # Placeholder, will fill below
        "hazardGrid": [[0]*60 for _ in range(60)],
        "start": [10, 5],
        "end": [10, 55],
        "description": "Navigate through a narrow strait with strong currents."
    },
    "2": {
        "name": "Island Archipelago",
        "width": 60,
        "height": 60,
        "landGrid": [[0]*60 for _ in range(60)],
        "hazardGrid": [[0]*60 for _ in range(60)],
        "start": [30, 5],
        "end": [30, 55],
        "description": "Complex island chain with storm potential."
    }
}

# Fill some demo data roughly
# Demo 1: Strait
for r in range(60):
    for c in range(60):
        if (r < 20 or r > 40) and 20 < c < 40:
            DEMOS["1"]["landGrid"][r][c] = 1

# Demo 2: Archipelago
import random
random.seed(42)
for _ in range(15):
    cr, cc = random.randint(10, 50), random.randint(10, 50)
    for r in range(max(0, cr-3), min(60, cr+3)):
        for c in range(max(0, cc-3), min(60, cc+3)):
            DEMOS["2"]["landGrid"][r][c] = 1
# Hazards for Demo 2
for r in range(10, 20):
    for c in range(10, 20):
        DEMOS["2"]["hazardGrid"][r][c] = 1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demos', methods=['GET'])
def get_demos():
    # Return list of summaries
    summary = []
    for k, v in DEMOS.items():
        summary.append({
            "id": k,
            "name": v["name"],
            "description": v["description"]
        })
    return jsonify(summary)

@app.route('/load_demo/<demo_id>', methods=['GET'])
def load_demo(demo_id):
    if demo_id in DEMOS:
        return jsonify(DEMOS[demo_id])
    return jsonify({"error": "Demo not found"}), 404

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    width = data.get('width', 50)
    height = data.get('height', 50)
    start = data.get('start') # [r, c]
    end = data.get('end')     # [r, c]
    land_grid = data.get('landGrid') # 2D array, 1=land, 0=water
    hazard_grid = data.get('hazardGrid') # 2D array, 1=hazard
    
    # Currents could be passed in, or simulated safely here if not provided
    # For this demo, let's generate simpler currents based on user params later, 
    # but for now, we can generate a default pattern if not provided fully.
    # Actually, let's re-generate the gyres logic from the original script 
    # BUT mapped to the new grid size, unless user passes vector field.
    # To keep payload small, we'll generate vectors here similar to original script.
    
    y, x = np.mgrid[0:height, 0:width]
    cy, cx = height // 2, width // 2
    
    # Default Gyre pattern
    current_u = -(y - cy) * 0.05 + np.sin(x/10)
    current_v = (x - cx) * 0.05 + np.cos(y/10)
    
    # If user wants to define flow, they could pass a grid of angles/magnitudes.
    # For simplicity MVP: Use the procedural field from the script.
    
    modes = ['fastest', 'fuel_efficient', 'coastal']
    results = {}
    
    for mode in modes:
        path = logic.run_astar(
            start, end, width, height, 
            np.array(land_grid), hazard_grid, current_u, current_v, 
            mode
        )
        if path:
            # Convert [(r, c), ...] to [[c, r], ...] for easier JS usage (x, y)
            results[mode] = [[c, r] for r, c in path]
        else:
            results[mode] = []

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
