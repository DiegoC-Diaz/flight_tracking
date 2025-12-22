from dotenv import load_dotenv
import os
import asyncio

from airportdb_service import AirportDBService
load_dotenv()
TOKEN=os.getenv("AIRPORT_DB_TOKEN")
ICAO="MHLM"

async def main():
    service=AirportDBService(token=TOKEN)
    data = await service.get_airport_data(ICAO)
    print(data)

if __name__ == "__main__":
    asyncio.run(main())
