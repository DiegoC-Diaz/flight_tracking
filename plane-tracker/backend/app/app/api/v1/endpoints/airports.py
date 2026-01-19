from typing import Annotated
from fastapi import APIRouter, Query
from asyncer import asyncify, create_task_group, syncify
from app.core.config import settings
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response
from app.core.dependencies import AirportServiceDep
from app.utils.mappers.airport_mapper import map_airport_from_airportdb

router = APIRouter()

@router.get("/info")
async def get_airport_info(
    icao: Annotated[str, Query(description="ICAO code of the airport")],
    airport_service: AirportServiceDep,
) -> IGetResponseBase:
    airport_data = await airport_service.get_airport_data(icao)
    print("airport_data:")
    print(airport_data)
    return create_response(data=airport_data, message="Airport data retrieved successfully")


@router.get("/closest")
async def get_closest_airports(
    latitude: Annotated[float, Query(description="Latitude of the reference point")],
    longitude: Annotated[float, Query(description="Longitude of the reference point")],
    limit: Annotated[int, Query(description="Number of closest airports to retrieve")],
    airport_service: AirportServiceDep,
) -> IGetResponseBase:
    closest_airports = await airport_service.get_closest_airports(latitude, longitude, limit)
    mapped_airports = [map_airport_from_airportdb(airport) for airport in closest_airports]
    return create_response(data=mapped_airports, message="Closest airports retrieved successfully")

@router.get("/by-area")
async def get_airports_by_area(
    lomin: Annotated[float, Query(description="Minimum longitude of the bounding box")],
    lamin: Annotated[float, Query(description="Minimum latitude of the bounding box")],
    lomax: Annotated[float, Query(description="Maximum longitude of the bounding box")],
    lamax: Annotated[float, Query(description="Maximum latitude of the bounding box")],
    airport_service: AirportServiceDep,
) -> IGetResponseBase:
    bbox = (lomin, lamin, lomax, lamax)
    airports_in_area = await airport_service.get_airports_by_area(bbox)
    
    return create_response(data=airports_in_area, message="Airports in area retrieved successfully")