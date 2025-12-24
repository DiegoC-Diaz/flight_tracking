from typing import Annotated
from fastapi import Depends
from app.services.airport_service import AirportService

def provide_airport_service() -> AirportService:
    return AirportService()

AirportServiceDep = Annotated[AirportService, Depends(provide_airport_service)]
