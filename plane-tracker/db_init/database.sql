CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE airports (
  id SERIAL PRIMARY KEY,
  icao CHAR(4) UNIQUE NOT NULL,
  iata CHAR(3),
  name TEXT NOT NULL,
  country TEXT,
  elevation_ft INTEGER,
  location GEOGRAPHY(Point, 4326)
);

CREATE INDEX idx_airports_location
ON airports
USING GIST (location);
