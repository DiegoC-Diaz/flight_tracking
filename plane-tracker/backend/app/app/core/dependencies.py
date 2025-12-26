from typing import Annotated
from fastapi import Depends
from app.services.airport_service import AirportService
from app.services.osky_service import OskyService


def provide_airport_service() -> AirportService:
    return AirportService()


def provide_osky_service()->OskyService:
    return OskyService()

OskyServiceDep=Annotated[OskyService,Depends(provide_osky_service)]
AirportServiceDep = Annotated[AirportService, Depends(provide_airport_service)]
