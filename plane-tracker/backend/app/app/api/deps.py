from typing import Annotated
from fastapi import Depends
from app.services.airportdb_service import AirportDBService


def provide_airport_service() -> AirportDBService:
    return AirportDBService()

AirportServiceDep = Annotated[AirportDBService, Depends(provide_airport_service)]
