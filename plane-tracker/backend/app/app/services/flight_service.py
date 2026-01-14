from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.flight_model import Flight
from sqlmodel import select,func
from sqlalchemy import cast
from geoalchemy2 import Geography
from datetime import datetime
class FlightService:
    """
    Docstring for FlightService3
    
    This handles flight data histpory from the postgresql database.
    """
    def __init__ (self, session:AsyncSession):
        
        self.session =session
    async def get_flight_by_icao24(self, icao24: str):
        """
        Retrieves flight data from the database by its ICAO24 code.

        Args:
            icao24: The ICAO24 code of the flight to retrieve.
        
        Returns:
            A Flight model instance or None if not found.
        """
        statement = select(Flight).where(Flight.icao24 == icao24)
        result =  self.session.exec(statement)
        return result.first()
    
    async def get_all_flights_on_area(self, bbox: tuple[float, float, float, float],timestamp:datetime):
        """
        Retrieves all flights within a specified bounding box.

        Args:
            bbox: A tuple containing (lon_min, lat_min, lon_max, lat_max)
        
        Returns:
            A list of Flight model instances within the bounding box.
        """
        # Use ST_MakeEnvelope for PostGIS geography type (lon_min, lat_min, lon_max, lat_max, 4326)
        bbox = func.ST_MakeEnvelope(bbox[0], bbox[1], bbox[2], bbox[3],4326)
    
        statement = select(Flight).where(
            func.ST_Intersects(Flight.location, cast(bbox, Geography)),
            Flight.time==timestamp   
        ).limit(1000)  # Limit to 1000 results to avoid overload
        result = await self.session.exec(statement)
        return result.all()
        
        
    async def get_flight_path_by_aircraft(self,icao24:str, start:datetime, end:datetime):
        """
        Retrieves the flight path for a specific aircraft within a time interval.

        Args:
            icao24: The ICAO24 code of the aircraft.
            start: The start datetime of the interval.
            end: The end datetime of the interval.
        Returns: 
            A list of Flight with their current vector data.
        """
        
        statement = select(Flight).where(
            Flight.icao24 == icao24,
            Flight.time >= start,
            Flight.time <= end
        ).order_by(Flight.time)
        result = await self.session.exec(statement)
        return result.all()
    