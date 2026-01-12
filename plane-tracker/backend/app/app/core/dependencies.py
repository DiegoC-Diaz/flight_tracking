from typing import Annotated
from fastapi import Depends
from app.services.airport_service import AirportService
from app.services.osky_service import OskyService
from app.services.flight_service import FlightService
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession  # ¡Importa AsyncSession!

# Nota: Si AirportService u OskyService necesitan acceso a la base de datos,
# necesitarás inyectarles la sesión aquí. Por ahora, asumimos que no.
def provide_airport_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> AirportService:
    """
    Provides an AirportService with a database session dependency.
    """
    return AirportService(session=db_session)

def provide_osky_service() -> OskyService:
    return OskyService()

def provide_flight_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> FlightService:
    """
    Provides a FlightService with a database session dependency.
    """
    return FlightService(session=db_session)

OskyServiceDep = Annotated[OskyService, Depends(provide_osky_service)]
AirportServiceDep = Annotated[AirportService, Depends(provide_airport_service)]
FlightServiceDep = Annotated[FlightService, Depends(provide_flight_service)]

