
## ICAO CODEs:
MHLM: Ramón Villeda Morales International Airport (San Pedro Sula)
MHPR: Palmerola International Airport / Soto Cano Air Base (Comayagua/Tegucigalpa)
MHLC: Goloson International Airport (La Ceiba)
MHRO: Juan Manuel Gálvez International Airport (Roatan)



```



flights = api.get_flights_from_interval(start_time, end_time)
if flights:
    data = []
    for flight in flights:
        data.append({
            "icao24": flight.icao24,
            "firstSeen": flight.firstSeen,
            "estDepartureAirport": flight.estDepartureAirport,
            "lastSeen": flight.lastSeen,
            "estArrivalAirport": flight.estArrivalAirport,
            "callsign": flight.callsign,
            "estDepartureAirportHorizDistance": flight.estDepartureAirportHorizDistance,
            "estDepartureAirportVertDistance": flight.estDepartureAirportVertDistance,
            "estArrivalAirportHorizDistance": flight.estArrivalAirportHorizDistance,
            "estArrivalAirportVertDistance": flight.estArrivalAirportVertDistance,
            "departureAirportCandidatesCount": flight.departureAirportCandidatesCount,
            "arrivalAirportCandidatesCount": flight.arrivalAirportCandidatesCount
        })
    df = pd.DataFrame(data)
    df.to_csv("flights.csv", index=False)
    print(f"Vuelos recuperados: {len(flights)}. Guardado en flights.csv")
else:
    print("Vuelos recuperados: 0")

```