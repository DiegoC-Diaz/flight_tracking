
## ICAO CODEs:
MHLM: Ramón Villeda Morales International Airport (San Pedro Sula)
MHPR: Palmerola International Airport / Soto Cano Air Base (Comayagua/Tegucigalpa)
MHLC: Goloson International Airport (La Ceiba)
MHRO: Juan Manuel Gálvez International Airport (Roatan)

## Arquitectura del Proyecto

El proyecto sigue una **Arquitectura en Capas**, diseñada para separar responsabilidades y facilitar el mantenimiento:

- **Capa de Presentación (`app/api`)**:
  - Responsable de definir los endpoints (rutas) de la API.
  - Maneja la entrada y salida de datos HTTP.
  - Utiliza inyección de dependencias para acceder a los servicios.

- **Capa de Lógica de Negocio (`app/services`)**:
  - Contiene la lógica central de la aplicación.
  - Se encarga de la comunicación con APIs externas (como OpenSky y AirportDB).
  - Procesa los datos antes de devolverlos a la capa de presentación.

- **Capa de Configuración (`app/core`)**:
  - Centraliza la configuración del proyecto (variables de entorno, constantes).
  - Define modelos de configuración global.

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