# src/api/fastapi_app.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import asyncio

from src.api.schema import (
    RouteRequest, RouteResponse,
    ObstacleRequest, ObstacleResponse
)

from src.core_engine.get_path import get_shortest_path
from src.core_engine.simulate_route import simulate_route
from src.core_engine.check_obstacles import is_obstacle
from src.core_engine.navigator import Navigator
from src.pathfinding.reroute import reroute

app = FastAPI(
    title="NavyShip Navigation API",
    description="Routing, simulation, dynamic navigation, and obstacle detection backend",
    version="2.0.0"
)

# ======================================================
# 1️⃣ Shortest path
# ======================================================

@app.post("/route", response_model=RouteResponse)
def route(data: RouteRequest):
    result = get_shortest_path(
        data.start_lat, data.start_lon,
        data.end_lat, data.end_lon
    )
    return RouteResponse(**result)

# ======================================================
# 2️⃣ Simulated route
# ======================================================

@app.post("/simulate")
def simulate(data: RouteRequest):
    path_ids, coords, dist, status = simulate_route(
        data.start_lat, data.start_lon,
        data.end_lat, data.end_lon
    )

    return {
        "status": status,
        "distance_km": dist,
        "path_latlon": coords,
        "path_node_ids": path_ids
    }

# ======================================================
# 3️⃣ Obstacle check
# ======================================================

@app.post("/obstacle", response_model=ObstacleResponse)
def obstacle_check(data: ObstacleRequest):
    blocked = is_obstacle(data.lat, data.lon)
    return ObstacleResponse(is_blocked=blocked)

# ======================================================
# 4️⃣ LIVE NAVIGATION STREAM (SSE) ✅
# ======================================================

@app.get("/navigate_stream")
async def navigate_stream(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
    nav = Navigator()

    async def event_generator():
        start_id, goal_id, path, dist, status = nav.compute_initial_route(
            start_lat, start_lon,
            end_lat, end_lon
        )

        if path is None:
            yield "event: error\ndata: {\"message\": \"No path found\"}\n\n"
            return

        total_nodes = len(path)

        yield (
            "event: init\n"
            f"data: {json.dumps({'status': status, 'distance_km': dist, 'nodes': total_nodes})}\n\n"
        )

        index = 0

        while index < len(path):
            node_id = path[index]
            lat = nav.nodes[node_id]["lat"]
            lon = nav.nodes[node_id]["lon"]

            yield (
                "event: update\n"
                f"data: {json.dumps({'node': node_id, 'lat': lat, 'lon': lon, 'step': index + 1})}\n\n"
            )

            await asyncio.sleep(nav.sleep)

            if nav.obstacle_engine.obstacle_checker(lat, lon):
                yield "event: reroute\ndata: {\"message\": \"Obstacle detected\"}\n\n"

                new_path, new_dist, new_status = reroute(
                    node_id, goal_id,
                    nav.nodes, nav.adj,
                    obstacle_checker=nav.obstacle_engine.obstacle_checker,
                    threshold_km=nav.threshold
                )

                if new_path is None:
                    yield "event: error\ndata: {\"message\": \"Reroute failed\"}\n\n"
                    return

                path = new_path
                total_nodes = len(path)
                index = 0

                yield (
                    "event: reroute_success\n"
                    f"data: {json.dumps({'new_nodes': total_nodes, 'status': new_status})}\n\n"
                )
                continue

            index += 1

        yield "event: done\ndata: {\"message\": \"Destination reached\"}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
