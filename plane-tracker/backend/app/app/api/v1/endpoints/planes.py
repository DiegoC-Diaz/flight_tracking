from fastapi import APIRouter, Depends,Query,Path
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest, TimeIntervalParams
from app.core.dependencies import OskyServiceDep
from app.core.dependencies import FlightServiceDep
from app.utils.mappers.vector_mapper import map_vector_from_osky
from typing import Annotated
from datetime import datetime
router = APIRouter()

@router.get("/vectors")
def get_vectors_for_plane() -> IGetResponseBase:
    return create_response(data=[], message="Vectors retrieved successfully")

@router.get("/vectors/area")
async def get_vectors_in_area(osky_service: OskyServiceDep, vector_request: VectorRequest = Depends()) -> IGetResponseBase:
    # The service expects a tuple: (lomin, lamin, lomax, lamax)
    bbox = (
        vector_request.lomin,
        vector_request.lamin,
        vector_request.lomax,
        vector_request.lamax,
    )
    osky_data = await osky_service.get_state_vectors_area(bbox=bbox)
    mapped_data = map_vector_from_osky(osky_data)
    return create_response(data=mapped_data.model_dump(), message="Vectors in area retrieved successfully")

@router.get("/flights/area")
async def get_flights_in_area(flight_service: FlightServiceDep, vector_request: VectorRequest = Depends()) -> IGetResponseBase:
    # The service expects a tuple: (lomin, lamin, lomax, lamax)
    bbox = (
        vector_request.lomin,
        vector_request.lamin,
        vector_request.lomax,
        vector_request.lamax,
    )
    parsed_datetime=datetime.fromtimestamp(vector_request.timestamp)
    flight_data=await  flight_service.get_all_flights_on_area(bbox=bbox, timestamp=parsed_datetime) 
    return create_response(data=flight_data, message="Flights in area retrieved successfully")


@router.get("/flights/{icao}/track")
async def get_flight_path(icao:Annotated[str,Path(description="ICAO24 for Aircraft")], flight_service:FlightServiceDep, time_interval: TimeIntervalParams = Depends())-> IGetResponseBase:
    
    start=datetime.fromtimestamp(time_interval.start)
    end=datetime.fromtimestamp(time_interval.end)
    flight_path=await flight_service.get_flight_path_by_aircraft(icao24=icao, start=start, end=end)
    
    return create_response(data=flight_path, message="Flight path retrieved successfully")

@router.get("/vector")
async def get_vector_for_plane(icao: Annotated[str, Path(description="ICAO24 for Aircraft")], osky_service: OskyServiceDep) -> IGetResponseBase:
    response=await osky_service.get_state_vector_from_flight(icao)
    return create_response(data=response, message="Vector retrieved successfully")