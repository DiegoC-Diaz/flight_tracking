import pandas as pd

# Load original cleaned file
df = pd.read_csv("airports_cleaned.csv")

# Build PostGIS geography POINT (lon lat)
df["location"] = (
    "SRID=4326;POINT(" 
    + df["longitude"].astype(str) 
    + " " 
    + df["latitude"].astype(str) 
    + ")"
)

# Rename altitude → elevation_ft
df = df.rename(columns={
    "altitude": "elevation_ft"
})

# Select ONLY columns needed by DB
df_db = df[[
    "icao",
    "iata",
    "name",
    "country",
    "elevation_ft",
    "location"
]]

# Export CSV for migration
df_db.to_csv("airports_db_ready.csv", index=False)
