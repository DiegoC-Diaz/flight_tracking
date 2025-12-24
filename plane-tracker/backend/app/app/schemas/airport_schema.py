from app.schemas.response_schema import IGetResponseBase
from pydantic import BaseModel
from typing import List

class AirportOut(BaseModel):
    id:str
    icue:str
    location:str|None
    

    
class AirportResponse(IGetResponseBase[List[AirportOut]]):
    airports:List[AirportOut]


