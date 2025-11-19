from opensky_api import OpenSkyApi
from datetime import datetime

# NOTA: Per l'API OpenSky, l'ora inserita dall'utente DEVE essere intesa come UTC
# per evitare errori nei risultati, anche se qui non viene forzata esplicitamente.

# --- INPUT INTERATTIVO ---


def get_data(icao_code, start_str):
   print("--- Inserimento Dati Volo ---")
   icao_code =icao_code.strip().upper() #input("Inserisci l'identificativo ICAO dell'aeroporto (es. EDDF): ").strip().upper()
   start_str = start_str.strip() #input("Inserisci data e ora INIZIALE (Formato: YYYY-MM-DD HH:MM:SS): ").strip()
   end_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #input("Inserisci data e ora FINALE (Formato: YYYY-MM-DD HH:MM:SS): ").strip()
   print("----------------------------")
# --- CONVERSIONE IN TIMESTAMP ---
   date_format = "%Y-%m-%d %H:%M:%S"

   try:
       # Parsing delle stringhe e conversione in timestamp UNIX (secondi)
       # Importante: Le ore vengono interpretate come ore locali e convertite,
       # ma l'API OpenSky richiede UTC. Inserisci l'ora UTC per risultati corretti.
       start_time = int(datetime.strptime(start_str, date_format).timestamp())
       end_time = int(datetime.strptime(end_str, date_format).timestamp())
       print(end_time)
       return icao_code, start_time, end_time
   except ValueError:
      print("\nERRORE: Formato data/ora non valido. Controlla il formato YYYY-MM-DD HH:MM:SS.")
      exit()

# --- CHIAMATE API ORIGINALI ---




   #print(f"Recupero dati per {icao_code}...")
def getArrives(api):
   lista = []
   # Metodi richiesti dalla documentazione
   icao_code, start_time, end_time = get_data("LIRF".strip().upper(), "2025-11-19 07:00:00".strip())
   arrivals = api.get_arrivals_by_airport(icao_code, start_time, end_time)

# --- OUTPUT DEI RISULTATI ORIGINALI ---
   print("\nArrivals:")
   if arrivals:
      for flight in arrivals:
        lista.append(flight)
   else:
      print("Nessun arrivo trovato.")
   return lista



def getDepartures(api):
    lista = []
    icao_code, start_time, end_time = get_data("LIRF".strip().upper(), "2025-11-19 07:00:00".strip())
    departures = api.get_departures_by_airport(icao_code, start_time, end_time)
    print("\nDepartures:")
    if departures:
       for flight in departures:
          lista.append(flight)
    else:
       print("Nessuna partenza trovata.")
    return lista