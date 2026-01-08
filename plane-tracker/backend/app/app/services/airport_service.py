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