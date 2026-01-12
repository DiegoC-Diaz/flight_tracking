from fastapi import APIRouter, Depends,Query
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest
from app.core.dependencies import OskyServiceDep
from app.core.dependencies import FlightServiceDep
from app.utils.mappers.vector_mapper import map_vector_from_osky
from typing import Annotated
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
    flight_data=await  flight_service.get_all_flights_on_area(bbox=bbox)
    
    
    return create_response(data=flight_data, message="Flights in area retrieved successfully")


@router.get("/vector")
async def get_vector_for_plane(icao: Annotated[str, Query(description="ICAO24 for Aircraft")], osky_service: OskyServiceDep) -> IGetResponseBase:
    response=await osky_service.get_state_vector_from_flight(icao)
    return create_response(data=response, message="Vector retrieved successfully")