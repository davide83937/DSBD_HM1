from datetime import datetime
import time
import requests


CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"



def get_token(client_id, client_secret):
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

#i = 0

def get_info_flight(token, airport, begin_ts, end_ts, type):
    #global i
    url = f"https://opensky-network.org/api/flights/{type}?airport={airport}&begin={begin_ts}&end={end_ts}"
    #url1 = f"https://opensky-network.org/api/flights/{type}?airpor={airport}&begin={begin_ts}&end={end_ts}"

    """ TEST """
    """if i < 3:
        url2 = url1
        i = i + 1
    else:
        url2 = url
        i = i + 1
        if i > 20:
            i = 0"""

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        #print(f"APPOSTO: {i}", flush=True)
        return resp.json()
    elif resp.status_code == 404:
        return []
    else:
        raise Exception(f"Errore {resp.status_code}: {resp.text}")



def get_data(start_str):
   start_str = start_str.strip()
   end_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   date_format = "%Y-%m-%d %H:%M:%S"
   try:
       start_time = int(datetime.strptime(start_str, date_format).timestamp())
       end_time = int(datetime.strptime(end_str, date_format).timestamp())
       return start_time, end_time
   except ValueError:
      exit()


def get_single_flight(token, icao24):
    """
    Recupera lo stato attuale di un singolo transponder ICAO24 per un check veloce.
    Aggiungiamo DEBUG per vedere se fallisce.
    """
    headers = {"Authorization": f"Bearer {token}"}
    time_now = int(time.time())

    # Endpoint states/all con filtro ICAO24
    url = f"https://opensky-network.org/api/states/all?icao24={icao24}&time={time_now}"

    # DEBUG: Stampa l'URL esatto che stai chiamando
    print(f"DEBUG FALLBACK URL: {url}", flush=True)

    resp = requests.get(url, headers=headers)

    # DEBUG: Stampa il codice di stato prima di sollevare l'errore
    print(f"DEBUG FALLBACK STATUS: {resp.status_code}", flush=True)

    resp.raise_for_status()  # Solleva un'eccezione se lo stato HTTP non è 2xx

    return resp.json().get('states', [])