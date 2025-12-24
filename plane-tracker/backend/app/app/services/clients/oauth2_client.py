"""
OpenSky Network Service con cliente OAuth2 asíncrono y refresh automático.
"""

import os
import time
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")


class AsyncOAuth2Client:
    """
    Cliente OAuth2 asíncrono genérico con refresh automático de tokens.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_endpoint: str,
        token: Optional[Dict[str, Any]] = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.token = token
        self._http_client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Context manager para usar con async with."""
        self._http_client = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cierra el cliente HTTP al salir del contexto."""
        if self._http_client:
            await self._http_client.aclose()
    
    def _get_client(self) -> httpx.AsyncClient:
        """Obtiene o crea el cliente HTTP."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client
    
    async def fetch_token(self) -> Dict[str, Any]:
        """
        Obtiene un nuevo token usando client_credentials flow.
        
        Returns:
            Dict con token_data incluyendo access_token, expires_in, etc.
        """
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        client = self._get_client()
        response = await client.post(
            self.token_endpoint,
            data=data,
            headers=headers
        )
        response.raise_for_status()
        
        token_data = response.json()
        
        # Agregar timestamp de expiración si viene expires_in
        if "expires_in" in token_data:
            token_data["expires_at"] = time.time() + token_data["expires_in"]
        
        self.token = token_data
        print(f"✓ Token obtenido. Expira en: {token_data.get('expires_in', 'N/A')} segundos")
        return token_data
    
    def is_token_expired(self, margin: int = 300) -> bool:
        """
        Verifica si el token está expirado o próximo a expirar.
        
        Args:
            margin: Margen de seguridad en segundos (default: 5 minutos)
            
        Returns:
            True si el token está expirado o no existe
        """
        if not self.token:
            return True
        
        if "expires_at" not in self.token:
            return False
        
        return time.time() >= (self.token["expires_at"] - margin)
    
    async def ensure_valid_token(self) -> None:
        """
        Asegura que hay un token válido, obteniendo uno nuevo si es necesario.
        """
        if self.is_token_expired():
            print("🔄 Token expirado o inexistente, obteniendo nuevo token...")
            await self.fetch_token()
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Obtiene los headers de autorización con Bearer token.
        
        Returns:
            Dict con el header Authorization
        """
        if not self.token or "access_token" not in self.token:
            raise ValueError("No hay token disponible. Llama a fetch_token() primero.")
        
        return {"Authorization": f"Bearer {self.token['access_token']}"}
    
    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """
        Realiza una petición HTTP con token automático.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL completa
            **kwargs: Argumentos adicionales para httpx
            
        Returns:
            httpx.Response
        """
        await self.ensure_valid_token()
        
        # Agregar headers de autenticación
        headers = kwargs.pop("headers", {})
        headers.update(self.get_auth_headers())
        
        client = self._get_client()
        response = await client.request(method, url, headers=headers, **kwargs)
        
        return response
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Petición GET con token automático."""
        return await self.request("GET", url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Petición POST con token automático."""
        return await self.request("POST", url, **kwargs)
    
    async def close(self):
        """Cierra el cliente HTTP."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None


class OpenSkyService:
    """
    Servicio para interactuar con OpenSky Network API usando OAuth2.
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or CLIENT_ID
        self.client_secret = client_secret or SECRET
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