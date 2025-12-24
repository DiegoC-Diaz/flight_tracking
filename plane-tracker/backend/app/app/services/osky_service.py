
import os
import time
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from app.services.clients.oauth2_client import AsyncOAuth2Client
from app.core.config import settings
class OskyService:
    """
    Servicio para interactuar con OpenSky Network API usando OAuth2.
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.SECRET
        self.base_url = "https://opensky-network.org/api"
        self.token_endpoint = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
        
        # Crear cliente OAuth2
        self.oauth_client = AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint=self.token_endpoint
        )
    
    async def __aenter__(self):
        """Context manager para usar con async with."""
        await self.oauth_client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cierra recursos al salir del contexto."""
        await self.oauth_client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def authenticate(self) -> Dict[str, Any]:
        """
        Autentica y obtiene un token de acceso.
        
        Returns:
            Token data
        """
        return await self.oauth_client.fetch_token()
    
    def get_token(self) -> Optional[str]:
        """
        Obtiene el access token actual.
        
        Returns:
            Access token o None si no existe
        """
        if self.oauth_client.token:
            return self.oauth_client.token.get("access_token")
        return None
    
    async def get_current_flights(
        self,
        hours_back: float = 1.0
    ) -> Dict[str, Any]:
        """
        Obtiene todos los vuelos actuales en un rango de tiempo.
        
        Args:
            hours_back: Horas hacia atrás desde ahora (default: 1 hora)
            
        Returns:
            JSON con datos de vuelos
        """
        url = f"{self.base_url}/flights/all"
        
        end_time = int(time.time())
        start_time = end_time - int(hours_back * 3600)
        
        params = {
            "begin": start_time,
            "end": end_time
        }
        
        response = await self.oauth_client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_state_vectors_area(
        self,
        bbox: tuple[float, float, float, float]
    ) -> Dict[str, Any]:
        """
        Obtiene vectores de estado de aeronaves en un área específica.
        
        Args:
            bbox: Tupla con (lon_min, lat_min, lon_max, lat_max)
            
        Returns:
            JSON con vectores de estado
        """
        url = f"{self.base_url}/states/all"
        
        params = {
            "lomin": bbox[0],
            "lamin": bbox[1],
            "lomax": bbox[2],
            "lamax": bbox[3],
        }
        
        response = await self.oauth_client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_all_state_vectors(self) -> Dict[str, Any]:
        """
        Obtiene todos los vectores de estado disponibles.
        
        Returns:
            JSON con vectores de estado
        """
        url = f"{self.base_url}/states/all"
        
        response = await self.oauth_client.get(url)
        response.raise_for_status()
        
        return response.json()
    
    async def close(self):
        """Cierra el cliente OAuth2."""
        await self.oauth_client.close()


# Ejemplo de uso
async def main():
    # Opción 1: Usar context manager (recomendado)
    async with OpenSkyService() as service:
        # Autenticar (opcional, se hace automáticamente en la primera petición)
        await service.authenticate()
        print(f"Token obtenido: {service.get_token()[:20]}...\n")
        
        # Obtener vuelos actuales (última hora)
        try:
            flights = await service.get_current_flights(hours_back=0.5)
            print(f"✓ Vuelos obtenidos: {len(flights)} registros")
        except httpx.HTTPError as e:
            print(f"✗ Error al obtener vuelos: {e}")
        
        # Obtener estado de aeronaves en un área (ejemplo: sobre Europa)
        try:
            bbox = (-10, 35, 20, 60)  # lon_min, lat_min, lon_max, lat_max
            states = await service.get_state_vectors_area(bbox)
            print(f"✓ Estados obtenidos: {states.get('time', 'N/A')}")
        except httpx.HTTPError as e:
            print(f"✗ Error al obtener estados: {e}")
    
    # Opción 2: Gestión manual
    # service = OpenSkyService()
    # await service.authenticate()
    # flights = await service.get_current_flights()
    # await service.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())