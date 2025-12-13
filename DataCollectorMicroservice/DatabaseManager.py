import os
from datetime import datetime, timedelta
import mysql.connector
import apiOpenSky as api
import kafka_services as k
import circuit_breaker
from circuit_breaker import CircuitBreakerOpenException



DEPARTURES_TABLE = "Flight_Data_Departures"
ARRIVALS_TABLE = "Flight_Data_Arrives"

producer = k.create_producer()
cb = circuit_breaker.CircuitBreaker()

def connect():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=3306,
        user="anto",
        password="onta",
        database="DataDB",
        autocommit=True
    )
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT DATABASE();")
    print("Connesso al DB:", cursor.fetchone())
    return conn, cursor

def disconnect(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()
    print("Connessione chiusa")


def check_count(row_count):
    if row_count > 0:
        return 0
    else:
        return 1

def insertInterests(email, airport_code, mode, h_value, l_value):
    conn = None
    cursor = None
    try:
       insert_query = f"INSERT INTO Interessi (email, airport, high_value, low_value, mode) VALUES (%s, %s, %s, %s, %s)"
       conn, cursor = connect()
       cursor.execute(insert_query, (email, airport_code, h_value, l_value, mode))
       return check_count(cursor.rowcount)
    except mysql.connector.Error as err:
        print(f"!!! ERRORE CRITICO SQL !!! : {err}", flush=True)
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)

def insertOnDatabase(lista, table):
    conn = None
    cursor = None
    try:
       insert_query = f"INSERT INTO {table} (Airport, Flight_code, Final_Airport, Departure_Time, Arrive_Time) VALUES (%s, %s, %s, %s, %s)"
       conn, cursor =connect()
       for flight in lista:
           try:
               aeroporto = (flight.get("estDepartureAirport") or "").strip()
               codice_volo = (flight.get("callsign") or "").strip()
               aeroporto_finale = (flight.get("estArrivalAirport") or "").strip()
               partenza_ts = flight.get("firstSeen")
               arrivo_ts = flight.get("lastSeen")
               partenza_dt = datetime.fromtimestamp(partenza_ts)
               arrivo_dt = datetime.fromtimestamp(arrivo_ts)
               cursor.execute(insert_query, (aeroporto, codice_volo, aeroporto_finale, partenza_dt, arrivo_dt))
           except mysql.connector.IntegrityError:
               updateFlight(cursor, table, aeroporto, codice_volo, partenza_dt, arrivo_dt)
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)

def updateFlight(cursor, table, aeroporto, codice_volo, partenza, arrivo):
    update_query = f"UPDATE {table} SET Arrive_Time = %s WHERE Flight_Code = %s AND Airport = %s AND Departure_Time = %s"
    cursor.execute(update_query, (arrivo, codice_volo, aeroporto, partenza))

def selectInterests():
    conn = None
    cursor = None
    try:
        query = "SELECT DISTINCT airport, mode FROM Interessi"
        conn, cursor = connect()
        cursor.execute(query)
        risultati = cursor.fetchall()
        return risultati
    except mysql.connector.Error as e:
        print(f"!!! ERRORE DB in selectInterests: {e}", flush=True)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

def deleteInterest(email, airport_code, mode):
    conn = None
    cursor = None
    try:
        delete_query = ""
        conn, cursor = connect()
        if(airport_code == ""):
            delete_query = "DELETE FROM Interessi WHERE email = %s"
            cursor.execute(delete_query, (email,))
        else:
            delete_query = "DELETE FROM Interessi WHERE email = %s AND airport = %s AND mode = %s"
            cursor.execute(delete_query, (email, airport_code, mode))
        if cursor.rowcount > 0:
            return 0
        else:
            return 1
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def download_flights(client_id, client_secret):
    lista_interessi = []
    response = selectInterests()
    if response == -1:
        return
    else:
        lista_interessi.extend(response)
    lista_partenze = []
    lista_arrivi = []
    aggiornamento_convalidato = True
    token = api.get_token(client_id, client_secret)
    start_time = datetime.now() - timedelta(days=1)
    start_time = int(start_time.timestamp())
    time_now = int(datetime.now().timestamp())
    for code, mode in lista_interessi:
      try:
        if mode:
            modalità = "departure"
            lista_partenze.extend(cb.call(api.get_info_flight,token, code, start_time, time_now, modalità))
        else:
            modalità = "arrival"
            lista_arrivi.extend(cb.call(api.get_info_flight,token, code, start_time, time_now, modalità))

      except CircuitBreakerOpenException:
          aggiornamento_convalidato = False
          raise
          #aggiornamento_convalidato = False
          #continue
      except Exception as e:
          print(f"Errore API OpenSky per {code}: {e}", flush=True)

          continue


      dati_salvati = False

      if lista_partenze:
            insertOnDatabase(lista_partenze, DEPARTURES_TABLE)
            dati_salvati = True

      if lista_arrivi:
            insertOnDatabase(lista_arrivi, ARRIVALS_TABLE)
            dati_salvati = True

      if dati_salvati:
            k.delivery_messagge(producer, k.topic1, k.message)





def delete_old_flights():
    conn = None
    cursor = None
    try:
        tables = ["Flight_Data_Arrives", "Flight_Data_Departures"]
        conn, cursor = connect()
        for table in tables:
            query = f"""DELETE FROM {table} WHERE STR_TO_DATE(Arrive_Time, '%Y-%m-%d %H:%i:%s') < (NOW() - INTERVAL 10 DAY)"""
            cursor.execute(query)
        return 0
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

def get_flight_by_airport(airport_code, mode):
    conn = None
    cursor = None
    try:
        conn, cursor = connect()
        get_query = ""
        if mode:
            get_query = "SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Departures WHERE Airport = %s"
        else:
            get_query = "SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Arrives WHERE Final_Airport = %s"
        cursor.execute(get_query, (airport_code,))
        result = cursor.fetchall()
        return result
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

def get_last_one(airport_code):
    conn = None
    cursor = None
    try:
        get_query = """
            SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Arrives 
            WHERE Final_Airport = %s 
            ORDER BY Arrive_Time DESC 
            LIMIT 1
        """
        conn, cursor = connect()
        cursor.execute(get_query, (airport_code,))
        last_arrival = cursor.fetchone()
        get_query = """
                    SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Departures 
                    WHERE Airport = %s 
                    ORDER BY Departure_Time DESC 
                    LIMIT 1
                """
        cursor.execute(get_query, (airport_code,))
        last_departure = cursor.fetchone()
        return last_arrival, last_departure
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def get_average_flights(airport_code, days):
    conn = None
    cursor = None
    try:
        conn, cursor = connect()
        if int(days) <= 0:
            return 0, 0

        avg_query = """
            SELECT COUNT(*) FROM Flight_Data_Arrives 
            WHERE Final_Airport = %s 
            AND Arrive_Time >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """
        cursor.execute(avg_query, (airport_code, int(days)))
        total_arrivals = cursor.fetchone()[0]

        avg_query = """
            SELECT COUNT(*) FROM Flight_Data_Departures 
            WHERE Airport = %s 
            AND Departure_Time >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """
        cursor.execute(avg_query, (airport_code, int(days)))
        total_departures = cursor.fetchone()[0]
        avg_arrivals = total_arrivals / int(days)
        avg_departures = total_departures / int(days)
        return avg_arrivals, avg_departures
    except mysql.connector.DatabaseError:
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def check_flight_conditions():
    conn = None
    cursor = None
    alerts = []  # Lista per salvare i risultati delle condizioni verificate

    try:
        conn, cursor = connect()

        # 1. Recupera tutti i profili di interesse
        # Assumiamo che la tabella Interessi abbia le colonne: email, airport, mode, high_value, low_value
        query_interessi = "SELECT email, airport, mode, high_value, low_value FROM Interessi"
        cursor.execute(query_interessi)
        interessi = cursor.fetchall()

        for profilo in interessi:
            email, airport, mode, high_val, low_val = profilo

            # 2. Determina quale tabella e quale colonna interrogare in base al 'mode'
            # Assunzione: mode 0 = Arrivi, mode 1 = Partenze
            if mode == 0:
                # Per gli arrivi cerchiamo 'Final_Airport' (destinazione) o 'Airport' se è l'aeroporto di riferimento
                # Basandomi sulla tua funzione precedente: Flight_Data_Arrives -> WHERE Final_Airport = %s
                table = "Flight_Data_Arrives"
                where_col = "Final_Airport"
            else:
                # Per le partenze: Flight_Data_Departures -> WHERE Airport = %s
                table = "Flight_Data_Departures"
                where_col = "Airport"

            # 3. Recupera i voli per contarli e ottenere le info
            query_voli = f"""
                SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code 
                FROM {table} 
                WHERE {where_col} = %s
            """
            cursor.execute(query_voli, (airport,))
            voli = cursor.fetchall()

            count = len(voli)
            condizione_superata = None

            # 4. Verifica le condizioni
            if count > high_val:
                condizione_superata = 'HIGH_VALUE_EXCEEDED'
            elif count < low_val:
                condizione_superata = 'LOW_VALUE_REACHED'

            # 5. Se una condizione è soddisfatta, salva le info
            if condizione_superata:
                alert_info = {
                    'email': email,
                    'airport': airport,
                    'mode': 'Arrivals' if mode == 0 else 'Departures',
                    'condition': condizione_superata,
                    'current_count': count,
                    'threshold': high_val if condizione_superata == 'HIGH_VALUE_EXCEEDED' else low_val,
                    'flights': voli  # Restituisce la lista delle tuple dei voli
                }
                alerts.append(alert_info)
        return alerts
    except mysql.connector.DatabaseError as err:
        print(f"Error: {err}")
        return -1
    finally:
        if conn is not None:
            disconnect(conn, cursor)


def check_fallback_api(client_id, client_secret):
    """
    Tenta di chiamare la API veloce per un singolo volo.
    Restituisce True se ha successo, False se il Circuit Breaker si apre.
    """
    try:
        token = api.get_token(client_id, client_secret)

        # Sostituisci "A4C9B4" con un codice ICAO di un volo noto che usi per il test
        # Stiamo usando il Circuit Breaker per proteggere anche questa API di check!
        cb.call(api.get_single_flight, token, "A4C9B4")

        # Se la chiamata ha successo e ritorna un risultato valido
        return True

    except CircuitBreakerOpenException:
        # Se il CB si apre qui, significa che anche l'API di check non funziona
        return False

    except Exception as e:
        # Qualsiasi altro errore (es. fallimento del token)
        print(f"Errore nel check fallback: {e}", flush=True)
        return False