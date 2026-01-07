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
    response = map_airport_from_airportdb(airport_data)
    return create_response(data=response, message="Airport data retrieved successfully")

@router.get("/all")
async def get_all_airports()->IGetResponseBase:
    #work in progess
    pass



@router.get("/test")
async def test_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com")
        data = response.json()
    return create_response(data=data, message="Test endpoint successful")

