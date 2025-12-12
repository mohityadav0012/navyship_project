from fastapi import FastAPI
from src.api.schema import RouteRequest, RouteResponse, ObstacleRequest, ObstacleResponse

from src.core_engine.get_path import get_shortest_path
from src.core_engine.simulate_route import simulate_route
from src.core_engine.check_obstacles import is_obstacle

app = FastAPI(
    title="NavyShip Navigation API",
    description="Routing, simulation, and obstacle detection backend",
    version="1.0.0"
)


@app.post("/route", response_model=RouteResponse)
def route(data: RouteRequest):

    result = get_shortest_path(
        data.start_lat, data.start_lon,
        data.end_lat, data.end_lon
    )

    return RouteResponse(**result)


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


@app.post("/obstacle", response_model=ObstacleResponse)
def obstacle_check(data: ObstacleRequest):

    blocked = is_obstacle(data.lat, data.lon)

    return ObstacleResponse(is_blocked=blocked)
