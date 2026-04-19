from typing import List, Dict, Any, Optional, Union
from app.models.flight_model import Flight
from app.schemas.vector_schema import VectorOut
from geoalchemy2.shape import to_shape
import json


class GeoJSONMapper:
    """
    Mapper to convert flight DTOs (Flight model and VectorOut) into GeoJSON format 
    for OpenLayers visualization.
    """
    
    @staticmethod
    def flight_to_geojson_feature(flight: Flight) -> Optional[Dict[str, Any]]:
        """
        Convert a single Flight model to a GeoJSON Feature.
        
        Args:
            flight: Flight model instance
            
        Returns:
            GeoJSON Feature dictionary or None if location is missing
        """
        if not flight.location:
            return None
            
        # Convert geography to coordinates
        point = to_shape(flight.location)
        coordinates = [point.x, point.y]
        
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            },
            "properties": {
                "icao24": flight.icao24,
                "callsign": flight.callsign,
                "velocity": flight.velocity,
                "heading": flight.heading,
                "vertrate": flight.vertrate,
                "onground": flight.onground,
                "alert": flight.alert,
                "spi": flight.spi,
                "squawk": flight.squawk,
                "baroaltitude": flight.baroaltitude,
                "geoaltitude": flight.geoaltitude,
                "time": flight.time.isoformat() if flight.time else None,
                "lastposupdate": flight.lastposupdate.isoformat() if flight.lastposupdate else None,
                "lastcontact": flight.lastcontact.isoformat() if flight.lastcontact else None
            }
        }
    
    @staticmethod
    def vector_to_geojson_feature(vector: VectorOut) -> Optional[Dict[str, Any]]:
        """
        Convert a single VectorOut to a GeoJSON Feature.
        
        Args:
            vector: VectorOut instance
            
        Returns:
            GeoJSON Feature dictionary or None if coordinates are missing
        """
        if vector.longitude is None or vector.latitude is None:
            return None
            
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [vector.longitude, vector.latitude]
            },
            "properties": {
                "icao24": vector.icao24,
                "callsign": vector.callsign,
                "origin_country": vector.origin_country,
                "time_position": vector.time_position,
                "baro_altitude": vector.baro_altitude,
                "category": vector.category
            }
        }
    
    @staticmethod
    def flights_to_geojson_feature_collection(flights: List[Flight]) -> Dict[str, Any]:
        """
        Convert a list of Flight models to a GeoJSON FeatureCollection.
        
        Args:
            flights: List of Flight model instances
            
        Returns:
            GeoJSON FeatureCollection dictionary
        """
        features = []
        for flight in flights:
            feature = GeoJSONMapper.flight_to_geojson_feature(flight)
            if feature:
                features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    @staticmethod
    def vectors_to_geojson_feature_collection(vectors: List[VectorOut]) -> Dict[str, Any]:
        """
        Convert a list of VectorOut instances to a GeoJSON FeatureCollection.
        
        Args:
            vectors: List of VectorOut instances
            
        Returns:
            GeoJSON FeatureCollection dictionary
        """
        features = []
        for vector in vectors:
            feature = GeoJSONMapper.vector_to_geojson_feature(vector)
            if feature:
                features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    @staticmethod
    def flight_path_to_geojson_feature(flights: List[Flight]) -> Optional[Dict[str, Any]]:
        """
        Convert a list of Flight models (same aircraft) to a LineString GeoJSON Feature.
        
        Args:
            flights: List of Flight model instances for the same aircraft
            
        Returns:
            GeoJSON Feature with LineString geometry or None if insufficient data
        """
        if len(flights) < 2:
            return None
            
        # Sort by time to ensure proper path order
        sorted_flights = sorted(flights, key=lambda f: f.time if f.time else datetime.min)
        
        coordinates = []
        properties = {
            "icao24": sorted_flights[0].icao24,
            "callsign": sorted_flights[0].callsign,
            "path_start": sorted_flights[0].time.isoformat() if sorted_flights[0].time else None,
            "path_end": sorted_flights[-1].time.isoformat() if sorted_flights[-1].time else None,
            "point_count": len(sorted_flights)
        }
        
        for flight in sorted_flights:
            if flight.location:
                point = to_shape(flight.location)
                coordinates.append([point.x, point.y])
        
        if len(coordinates) < 2:
            return None
            
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": properties
        }
    
    @staticmethod
    def to_geojson_string(geojson_data: Dict[str, Any]) -> str:
        """
        Convert GeoJSON dictionary to JSON string.
        
        Args:
            geojson_data: GeoJSON dictionary
            
        Returns:
            JSON string
        """
        return json.dumps(geojson_data, indent=2)
