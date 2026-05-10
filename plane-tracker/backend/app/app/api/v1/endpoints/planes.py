from fastapi import APIRouter, Depends,Query,Path
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest, TimeIntervalParams
from app.core.dependencies import OskyServiceDep
from app.core.dependencies import FlightServiceDep
from app.utils.mappers.vector_mapper import map_vector_from_osky
from app.utils.mappers.geojson_mapper import GeoJSONMapper
from typing import Annotated
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)
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
    parsed_datetime = datetime.fromtimestamp(vector_request.timestamp, tz=timezone.utc)
    logger.warning(
        "flights/area request bbox=%s timestamp_unix=%s timestamp_utc=%s",
        bbox,
        vector_request.timestamp,
        parsed_datetime.isoformat(),
    )
    logger.warning(
        "flights/area time_window start_utc=%s end_utc=%s",
        (parsed_datetime - timedelta(seconds=10)).isoformat(),
        (parsed_datetime + timedelta(seconds=10)).isoformat(),
    )

    flight_data = await flight_service.get_all_flights_on_area(bbox=bbox, timestamp=parsed_datetime)
    logger.warning(
        "flights/area result_count=%s timestamp_utc=%s",
        len(flight_data),
        parsed_datetime.isoformat(),
    )
    geojson_data = GeoJSONMapper.flights_to_geojson_feature_collection(flight_data)
    return create_response(data=geojson_data, message="Flights in area retrieved successfully")

@router.get("/flights/{icao}/track")
async def get_flight_path(icao:Annotated[str,Path(description="ICAO24 for Aircraft")], flight_service:FlightServiceDep, time_interval: TimeIntervalParams = Depends())-> IGetResponseBase:
    
    start=datetime.fromtimestamp(time_interval.start)
    end=datetime.fromtimestamp(time_interval.end)
    flight_path=await flight_service.get_flight_path_by_aircraft(icao24=icao, start=start, end=end)
    geojson_data = GeoJSONMapper.flight_path_to_geojson_feature(flight_path)
    
    return create_response(data=geojson_data, message="Flight path retrieved successfully")

@router.get("/vector")
async def get_vector_for_plane(icao: Annotated[str, Path(description="ICAO24 for Aircraft")], osky_service: OskyServiceDep) -> IGetResponseBase:
    response=await osky_service.get_state_vector_from_flight(icao)
    return create_response(data=response, message="Vector retrieved successfully")
