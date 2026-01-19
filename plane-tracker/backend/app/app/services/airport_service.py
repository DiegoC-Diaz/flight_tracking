from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.airport_model import Airport 

class AirportService:
    """
    This service handles database operations related to airports.
    It's designed to be initialized with a database session.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the AirportService with a database session.

        Args:
            session: An asynchronous database session.
        """
        self.session = session

    async def get_airport_data(self, icao: str):
        """
        Retrieves airport data from the database by its ICAO code.

        Args:
            icao: The ICAO code of the airport to retrieve.
        
        Returns:
            An Airport model instance or None if not found.
        """
        statement = select(Airport).where(Airport.icao == icao)
        
        result = await self.session.exec(statement)

        return result.first()
    
    async def get_closest_airports(self, latitude: float, longitude: float, limit: int = 10):
        """
        Retrieves the closest airports to a given latitude and longitude using PostGIS geospatial queries.

        Args:
            latitude: The latitude to search from.
            longitude: The longitude to search from.
            limit: The maximum number of airports to return.
        """
        from sqlalchemy import func
        statement = select(Airport).order_by(
            func.ST_Distance(
                Airport.location,
                func.ST_MakePoint(longitude, latitude)
            )
        ).limit(limit)
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_airports_by_area(self, bbox: tuple[float, float, float, float]):
        """
        Retrieves all airports within a specified bounding box using PostGIS geospatial queries.

        Args:
            bbox: A tuple containing (lon_min, lat_min, lon_max, lat_max)
        
        Returns:
            A list of Airport model instances within the bounding box.
        """
        from sqlalchemy import func
        lon_min, lat_min, lon_max, lat_max = bbox
        envelope = func.ST_MakeEnvelope(lon_min, lat_min, lon_max, lat_max, 4326)
        statement = select(Airport).where(
            func.ST_Within(func.ST_GeomFromWKB(Airport.location), envelope)
        )
        result = await self.session.exec(statement)
        return result.all()