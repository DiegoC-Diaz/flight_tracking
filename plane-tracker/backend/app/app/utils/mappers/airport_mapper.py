from app.schemas.airport_schema import AirportOut
from app.schemas.airport_schema import AirportResponse

def map_airport_from_airportdb(airportdb_data:dict) -> AirportOut:
    return AirportOut.model_validate(airportdb_data)



def map_airports_from_airportdb_list(airportdb_list:list[dict]) -> list[AirportOut]:
    
    if not airportdb_list or len(airportdb_list) == 0:
        return AirportResponse(airports=[])
    airport_list = [map_airport_from_airportdb(airport) for airport in airportdb_list]
    return AirportResponse(airports=airport_list)
    
    