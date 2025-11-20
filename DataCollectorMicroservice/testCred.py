from opensky_api import OpenSkyApi
from datetime import datetime
import requests

# NOTA: Per l'API OpenSky, l'ora inserita dall'utente DEVE essere intesa come UTC
# per evitare errori nei risultati, anche se qui non viene forzata esplicitamente.

# --- INPUT INTERATTIVO ---
# --- CONFIGURAZIONE ---
CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"
AIRPORT = "LICC"

# --- FUNZIONI ---
def get_token(client_id, client_secret):
    """Ottieni token Bearer da OpenSky"""
    url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]



def get_info_flight(token, airport, begin_ts, end_ts, type):
    """Recupera arrivi dall'API OpenSky per un intervallo"""
    url = f"https://opensky-network.org/api/flights/{type}?airport={airport}&begin={begin_ts}&end={end_ts}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 404:
        return []  # nessun volo in questo intervallo
    else:
        raise Exception(f"Errore {resp.status_code}: {resp.text}")



def get_data(start_str):
   #icao_code =icao_code.strip().upper() #input("Inserisci l'identificativo ICAO dell'aeroporto (es. EDDF): ").strip().upper()
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
       return start_time, end_time
   except ValueError:
      print("\nERRORE: Formato data/ora non valido. Controlla il formato YYYY-MM-DD HH:MM:SS.")
      exit()






   #print(f"Recupero dati per {icao_code}...")
"""def getArrives(api):
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
   return lista"""



"""def getDepartures(api):
    lista = []
    icao_code, start_time, end_time = get_data("LIRF".strip().upper(), "2025-11-19 07:00:00".strip())
    departures = api.get_departures_by_airport(icao_code, start_time, end_time)
    print("\nDepartures:")
    if departures:
       for flight in departures:
          lista.append(flight)
    else:
       print("Nessuna partenza trovata.")
    return lista """