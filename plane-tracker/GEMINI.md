
## Return Types


**class opensky_api.FlightData(arr)**

Class that represents data of certain flight. It has the following fields:
icao24: str - Unique ICAO 24-bit address of the transponder in hex string representation. All letters are lower case.
firstSeen: int - Estimated time of departure for the flight as Unix time (seconds since epoch).
estDepartureAirport: str - ICAO code of the estimated departure airport. Can be null if the airport could not be identified.
lastSeen: int - Estimated time of arrival for the flight as Unix time (seconds since epoch).
estArrivalAirport: str - ICAO code of the estimated arrival airport. Can be null if the airport could not be identified.
callsign: str - Callsign of the vehicle (8 chars). Can be null if no callsign has been received. If the vehicle transmits multiple callsigns during the flight, we take the one seen most frequently.
estDepartureAirportHorizDistance: int - Horizontal distance of the last received airborne position to the estimated departure airport in meters.
estDepartureAirportVertDistance: int - Vertical distance of the last received airborne position to the estimated departure airport in meters.
estArrivalAirportHorizDistance: int - Horizontal distance of the last received airborne position to the estimated arrival airport in meters.
estArrivalAirportVertDistance: int - Vertical distance of the last received airborne position to the estimated arrival airport in meters.
departureAirportCandidatesCount: int - Number of other possible departure airports. These are airports in short distance to estDepartureAirport.
arrivalAirportCandidatesCount: int - Number of other possible departure airports.


Example:
Executing this will return a list of flights 
```
flights = api.get_flights_from_interval(start_time, end_time)

```