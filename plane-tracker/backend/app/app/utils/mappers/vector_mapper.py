from app.schemas.vector_schema import  VectorOut,VectorsResponse
from typing import List, Optional

def _map_single_vector_from_state(state: list) -> Optional[Vector]:
    """
    Maps a single state vector list from OpenSky to a Vector object.
    Returns None if the state list is malformed.
    """
    # Ensure the state list is long enough to avoid index errors
    if len(state) < 18:
        return None

    # OpenSky Index Mapping:
    # 0: icao24, 1: callsign, 2: origin_country, 3: time_position,
    # 5: longitude, 6: latitude, 7: baro_altitude, 17: category
    vector_data = {
        "icao24": state[0],
        "callsign": state[1],
        "origin_country": state[2],
        "time_position": state[3],
        "longitude": state[5],
        "latitude": state[6],
        "baro_altitude": state[7],
        "category": state[17],
    }
    return VectorOut.model_validate(vector_data)

def map_vector_from_osky(osky_data: dict) -> VectorOut:
    """
    Maps the state vectors from OpenSky API response to a VectorOut schema
    by processing a list of state vectors.
    """

    state_vectors = osky_data.get("states")

    if not state_vectors:
        return VectorOut(vectors=[])

    # Use a list comprehension with the helper function, filtering out None results
    vector_list = [
        mapped_vector
        for state in state_vectors
        if (mapped_vector := _map_single_vector_from_state(state)) is not None
    ]

    return VectorsResponse(vectors=vector_list)
