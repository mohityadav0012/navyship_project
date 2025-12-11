import math

EARTH_RADIUS_KM=6371.0088

def haversine_km(lat1,lon1,lat2,lon2):
    '''calculate the dis in km between two lat/lon points'''
    phi1,phi2=math.radians(lat1),math.radians(lat2)
    dphi=math.radians(lat2-lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))

def grid_index_to_coord(lat_min, lon_min, i, j, res): 
    '''Convert a grid cell index (i, j) into its real latitude & longitude.'''
    lat = lat_min + i * res
    lon = lon_min + j * res
    return lat, lon

def coord_to_grid_index(lat_min, lon_min, lat, lon, res):
    """Convert lat/lon to nearest grid i,j index (rounded)."""
    i = int(round((lat - lat_min) / res))
    j = int(round((lon - lon_min) / res))
    return i, j

