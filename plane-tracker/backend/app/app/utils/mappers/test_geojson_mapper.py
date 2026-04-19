"""
Test script for GeoJSON mapper functionality.
This demonstrates how to convert flight DTOs to GeoJSON format for OpenLayers.
"""
from datetime import datetime
from app.utils.mappers.geojson_mapper import GeoJSONMapper
from app.schemas.vector_schema import VectorOut
from geoalchemy2.elements import WKBElement
from geoalchemy2.functions import ST_Point


def create_mock_flight_data():
    """Create mock flight data for testing"""
    # This would normally come from your database
    # For testing, we'll create a mock flight with location data
    
    # Note: In real usage, you'd get Flight objects from your database
    # The location field would be a Geography/PostGIS point
    
    flights = []
    
    # Mock flight 1 - with location
    flight1 = type('MockFlight', (), {
        'icao24': 'ABC123',
        'callsign': 'UAL123',
        'velocity': 450.5,
        'heading': 90.0,
        'vertrate': 0.0,
        'onground': False,
        'alert': False,
        'spi': False,
        'squawk': '1234',
        'baroaltitude': 35000.0,
        'geoaltitude': 35200.0,
        'time': datetime.now(),
        'lastposupdate': datetime.now(),
        'lastcontact': datetime.now(),
        'location': ST_Point(-122.4194, 37.7749)  # San Francisco coordinates
    })()
    
    # Mock flight 2 - with location
    flight2 = type('MockFlight', (), {
        'icao24': 'DEF456',
        'callsign': 'AA456',
        'velocity': 380.0,
        'heading': 180.0,
        'vertrate': -500.0,
        'onground': False,
        'alert': False,
        'spi': False,
        'squawk': '5678',
        'baroaltitude': 28000.0,
        'geoaltitude': 28100.0,
        'time': datetime.now(),
        'lastposupdate': datetime.now(),
        'lastcontact': datetime.now(),
        'location': ST_Point(-74.0060, 40.7128)  # New York coordinates
    })()
    
    return [flight1, flight2]


def create_mock_vector_data():
    """Create mock vector data for testing"""
    vectors = [
        VectorOut(
            icao24="ABC123",
            callsign="UAL123",
            origin_country="United States",
            time_position=int(datetime.now().timestamp()),
            longitude=-122.4194,
            latitude=37.7749,
            baro_altitude=35000.0,
            category=3
        ),
        VectorOut(
            icao24="DEF456",
            callsign="AA456",
            origin_country="United States",
            time_position=int(datetime.now().timestamp()),
            longitude=-74.0060,
            latitude=40.7128,
            baro_altitude=28000.0,
            category=3
        )
    ]
    return vectors


def test_flight_to_geojson():
    """Test converting Flight models to GeoJSON"""
    print("=== Testing Flight to GeoJSON ===")
    
    flights = create_mock_flight_data()
    
    # Test single flight
    if flights:
        feature = GeoJSONMapper.flight_to_geojson_feature(flights[0])
        print("Single Flight Feature:")
        print(GeoJSONMapper.to_geojson_string(feature))
        print()
    
    # Test multiple flights as FeatureCollection
    feature_collection = GeoJSONMapper.flights_to_geojson_feature_collection(flights)
    print("Flight FeatureCollection:")
    print(GeoJSONMapper.to_geojson_string(feature_collection))
    print()


def test_vector_to_geojson():
    """Test converting VectorOut to GeoJSON"""
    print("=== Testing VectorOut to GeoJSON ===")
    
    vectors = create_mock_vector_data()
    
    # Test single vector
    if vectors:
        feature = GeoJSONMapper.vector_to_geojson_feature(vectors[0])
        print("Single Vector Feature:")
        print(GeoJSONMapper.to_geojson_string(feature))
        print()
    
    # Test multiple vectors as FeatureCollection
    feature_collection = GeoJSONMapper.vectors_to_geojson_feature_collection(vectors)
    print("Vector FeatureCollection:")
    print(GeoJSONMapper.to_geojson_string(feature_collection))
    print()


def test_flight_path_to_geojson():
    """Test converting flight path to LineString"""
    print("=== Testing Flight Path to GeoJSON ===")
    
    # Create multiple points for the same aircraft
    flights = create_mock_flight_data()
    
    # Add more points for the same aircraft to create a path
    additional_points = [
        type('MockFlight', (), {
            'icao24': 'ABC123',
            'callsign': 'UAL123',
            'time': datetime.now(),
            'location': ST_Point(-118.2437, 34.0522)  # Los Angeles
        })(),
        type('MockFlight', (), {
            'icao24': 'ABC123',
            'callsign': 'UAL123',
            'time': datetime.now(),
            'location': ST_Point(-112.0740, 33.4484)  # Phoenix
        })()
    ]
    
    flights.extend(additional_points)
    
    # Filter flights for same aircraft
    abc123_flights = [f for f in flights if f.icao24 == 'ABC123']
    
    if len(abc123_flights) >= 2:
        path_feature = GeoJSONMapper.flight_path_to_geojson_feature(abc123_flights)
        print("Flight Path Feature:")
        print(GeoJSONMapper.to_geojson_string(path_feature))
        print()


if __name__ == "__main__":
    print("Testing GeoJSON Mapper for Flight Tracking")
    print("=" * 50)
    
    test_flight_to_geojson()
    test_vector_to_geojson()
    test_flight_path_to_geojson()
    
    print("=== Usage Examples for OpenLayers ===")
    print("""
# In your frontend/OpenLayers code:

// Load flight data as GeoJSON
const flightSource = new ol.source.Vector({
    features: new ol.format.GeoJSON().readFeatures(geoJsonData, {
        featureProjection: 'EPSG:3857'
    })
});

// Create flight layer
const flightLayer = new ol.layer.Vector({
    source: flightSource,
    style: new ol.style.Style({
        image: new ol.style.Icon({
            src: '/airplane-icon.png',
            scale: 0.5
        })
    })
});

// Add to map
map.addLayer(flightLayer);

// For flight paths (LineString)
const pathSource = new ol.source.Vector({
    features: new ol.format.GeoJSON().readFeatures(pathGeoJsonData, {
        featureProjection: 'EPSG:3857'
    })
});

const pathLayer = new ol.layer.Vector({
    source: pathSource,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#ff0000',
            width: 2
        })
    })
});
""")
