from typing import Optional, Any, List
from sqlmodel import SQLModel, Field
from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape # Required for conversion
from pydantic import field_serializer
import sqlalchemy as sa

class Airport(SQLModel, table=True):
    __tablename__ = "airports"

    id: Optional[int] = Field(default=None, primary_key=True)
    icao: str = Field(sa_column_kwargs={"unique": True})
    iata: Optional[str] = Field(default=None)
    name: str
    location: Any = Field(sa_column=sa.Column(Geography("POINT", srid=4326)))

    # This is the magic part that fixes your error
    @field_serializer("location")
    def serialize_location(self, location: Any) -> Optional[List[float]]:
        if location is None:
            return None
        # to_shape converts the WKBElement into a Shapely object
        point = to_shape(location)
        # Returns [longitude, latitude]
        return [point.x, point.y]

    class Config:
        arbitrary_types_allowed = True