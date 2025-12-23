import httpx
from dotenv import load_dotenv
import os
load_dotenv()




class AirportDBService:
    def __init__(self,token=None):
        self.base_url="https://airportdb.io/api/v1/airport"
        self.token=token
        if token is None:
            self.token=os.getenv("AIRPORT_DB_TOKEN")
        pass

    def set_token(self,token):
        self.token=token
    
    async def get_airport_data(self,icao):
        url=f'{self.base_url}/{icao}'
        params={"apiToken":self.token}
        
        
        async with httpx.AsyncClient() as client:
           response=await client.get(url,params=params)
           if response.is_error:
               raise Exception("Error al obtener los vuelos actuales")

           return response.json()
    
    

           
           
        
        
        
        















