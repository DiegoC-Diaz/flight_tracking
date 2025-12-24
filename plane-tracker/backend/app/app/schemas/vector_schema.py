from app.schemas.response_schema import IGetResponseBase
from pydantic import BaseModel
from typing import List


class Vector(BaseModel):
    icao24:str
    callsign:str|None
    origin_country:str
    time_position:int
    longitude:float|None
    latitude:float|None
    baro_altitude:float
    category:int

class VectorsOut(BaseModel):
    vectors: List[Vector]
    
    
class VectorRequest(BaseModel):
    lamin:float
    lomin:float
    lamax:float
    lomax:float
    pass