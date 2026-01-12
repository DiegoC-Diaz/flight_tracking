from typing import Optional, Any, List
from sqlmodel import SQLModel, Field
from geoalchemy2 import Geography
from geoalchemy2.shape import to_shape # Required for conversion
from pydantic import field_serializer
import sqlalchemy as sa
from datetime import datetime

class Flight(SQLModel, table=True):
    __tablename__ = "flight_history"

    time: datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), primary_key=True, nullable=False))
    icao24: str = Field(sa_column=sa.Column(sa.String(8), primary_key=True, nullable=False))
    location: Optional[Any] = Field(
        sa_column=sa.Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    )
    velocity: Optional[float] = Field(default=None, sa_column=sa.Column(sa.REAL))
    heading: Optional[float] = Field(default=None, sa_column=sa.Column(sa.REAL))
    vertrate: Optional[float] = Field(default=None, sa_column=sa.Column(sa.REAL))
    callsign: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String(10)))
    onground: Optional[bool] = Field(default=None, sa_column=sa.Column(sa.Boolean))
    alert: Optional[bool] = Field(default=None, sa_column=sa.Column(sa.Boolean))
    spi: Optional[bool] = Field(default=None, sa_column=sa.Column(sa.Boolean))
    squawk: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String(4)))
    baroaltitude: Optional[float] = Field(default=None, sa_column=sa.Column(sa.REAL))
    geoaltitude: Optional[float] = Field(default=None, sa_column=sa.Column(sa.REAL))
    lastposupdate: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True)))
    lastcontact: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True)))

    @field_serializer("location")
    def serialize_location(self, location: Any) -> Optional[List[float]]:
        if location is None:
            return None
        point = to_shape(location)
        return [point.x, point.y]

    class Config:
        arbitrary_types_allowed = True






