from typing import Annotated
from fastapi import APIRouter, Query
from asyncer import asyncify, create_task_group, syncify
from app.core.config import settings
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response
from app.api.deps import AirportServiceDep


router = APIRouter()

@router.get("/info")
async def get_airport_info(
    icao: Annotated[str, Query(description="ICAO code of the airport")],
    airport_service: AirportServiceDep,
) -> IGetResponseBase:
    airport_data = await airport_service.get_airport_data(icao)
    return create_response(data=airport_data, message="Airport data retrieved successfully")
