import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")
base_url = "https://opensky-network.org/api"


class OpenSkyService:
    def __init__(self, token=None):
        self.client_id = CLIENT_ID
        self.client_secret = SECRET
        self.base_url = base_url
        self.token = token
        self.auth_headers = None



    def set_token(self, token):
        self.token = token
        
        

    def get_token(self):        
        return self.token

    async def request_token(self):
        url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            return token_data["access_token"]

    async def get_current_flights(self):
        url = f"{self.base_url}/flights/all"
        auth_headers = {"Authorization": f"Bearer {self.token}"}
        
        start_time = int(time.time()) - 560  # 1 hora antes
        end_time = int(time.time())
        params = {"begin": start_time, "end": end_time}
        
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=auth_headers, params=params)

            if response.is_error:
                raise Exception("Error al obtener los vuelos actuales")
            return response.json()

    async def get_state_vectors_area(self, cors):
        api_url = f"{self.base_url}/states/all"
        auth_headers = {"Authorization": f"Bearer {self.token}"}

        params = {
            "lamin": cors[1],
            "lomin": cors[0],
            "lamax": cors[3],
            "lomax": cors[2],
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=auth_headers, params=params)

            if response.is_error:
                raise Exception("Error al obtener los vectores de estado en el área")
            return response.json()
