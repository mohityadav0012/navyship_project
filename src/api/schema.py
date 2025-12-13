# src/api/schema.py

from pydantic import BaseModel

class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float

class RouteResponse(BaseModel):
    status: str
    distance_km: float | None
    path_latlon: list
    path_node_ids: list

class ObstacleRequest(BaseModel):
    lat: float
    lon: float

class ObstacleResponse(BaseModel):
    is_blocked: bool
