from app.schemas.response_schema import IGetResponseBase
from pydantic import BaseModel
from typing import List

class AirportOut(BaseModel):
    ident:str
    type:str
    name:str
    iso_country:str
   
    

    
class AirportResponse(IGetResponseBase[List[AirportOut]]):
    airports:List[AirportOut]


