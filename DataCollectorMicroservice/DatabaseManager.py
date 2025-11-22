from datetime import datetime, timedelta
import mysql.connector
import testCred as api

DEPARTURES_TABLE = "Flight_Data_Departures"
ARRIVALS_TABLE = "Flight_Data_Arrives"


# Connessione al database
def connect():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="anto",
        password="onta",
        database="DataDB"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Connesso al DB:", cursor.fetchone())
    return conn, cursor

def disconnect(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()
    print("Connessione chiusa")


def insertInterests(email, airport_code, mode):
    try:

       insert_query = f"INSERT INTO Interessi (email, airport, mode) VALUES (%s, %s, %s)"
       conn, cursor = connect()
       cursor.execute(insert_query, (email, airport_code, mode))
       if cursor.rowcount > 0:
           return 0  # Successo (secondo la tua logica 0 = ok)
       else:
           return 1  # Fallimento (nessuna riga inserita)
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)

def insertOnDatabase(lista, table):
    try:
       insert_query = f"INSERT INTO {table} (Airport, Flight_code, Final_Airport, Departure_Time, Arrive_Time) VALUES (%s, %s, %s, %s, %s)"
       conn, cursor =connect()
       for flight in lista:
           aeroporto = (flight.get("estDepartureAirport") or "").strip()
           codice_volo = (flight.get("callsign") or "").strip()
           aeroporto_finale = (flight.get("estArrivalAirport") or "").strip()
           partenza_ts = flight.get("firstSeen")
           arrivo_ts = flight.get("lastSeen")

           # conversione timestamp → datetime
           partenza_dt = datetime.fromtimestamp(partenza_ts)
           arrivo_dt = datetime.fromtimestamp(arrivo_ts)

           cursor.execute(insert_query, (aeroporto, codice_volo, aeroporto_finale, partenza_dt, arrivo_dt))

    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)



def selectInterests():
    try:
        query = "SELECT DISTINCT airport, mode FROM Interessi"
        conn, cursor = connect()
        cursor.execute(query)
        # Scarica tutti i risultati in una lista
        risultati = cursor.fetchall()
        return risultati
        # 'risultati' sarà tipo: [('LIRF', 1), ('LICC', 0), ...]

    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

def deleteInterest(email, airport_code, mode):
    conn = None
    cursor = None
    try:
        # Query di cancellazione specifica
        delete_query = "DELETE FROM Interessi WHERE email = %s AND airport = %s AND mode = %s"
        conn, cursor = connect()  # Usa connect() se non hai 'self'
        cursor.execute(delete_query, (email, airport_code, mode))
        if cursor.rowcount > 0:
            print(f"Cancellato interesse per {email} su {airport_code}")
            return 0  # Successo
        else:
            print("Nessun interesse trovato da cancellare")
            return 1  # Nessuna riga trovata (o fallimento logico)
    except mysql.connector.Error as e:
        print(f"Errore DB durante cancellazione: {e}")
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def download_flights(client_id, client_secret):
    lista_interessi = []
    response = selectInterests()
    if response == -1:
        print("Errore")
        return
    else:
        lista_interessi.extend(response)
    lista_partenze = []
    lista_arrivi = []
    modalità = ""
    token = api.get_token(client_id, client_secret)
    start_time = datetime.now() - timedelta(days=1)
    start_time = int(start_time.timestamp())
    time_now = int(datetime.now().timestamp())
    for code, mode in lista_interessi:
        if mode:
            modalità = "departure"

            lista_partenze.extend(api.get_info_flight(token, code, start_time, time_now, modalità))

        else:
            modalità = "arrival"

            lista_arrivi.extend(api.get_info_flight(token, code, start_time, time_now, modalità))

    #insertOnDatabase(lista_partenze, DEPARTURES_TABLE)
    #insertOnDatabase(lista_arrivi, ARRIVALS_TABLE)



def delete_old_flights():
    conn = None
    cursor = None
    try:
        # Definisco le due tabelle da pulire
        tables = ["Flight_Data_Arrives", "Flight_Data_Departures"]

        # Connessione al DB (se hai ancora 'self' nella definizione di connect, usa connect(None))
        conn, cursor = connect()
        for table in tables:
            # Usiamo 'Arrive_Time' come riferimento temporale per decidere se il volo è vecchio
            # La query converte la stringa in data e controlla se è più vecchia di 2 giorni fa
            query = f"""
                DELETE FROM {table} 
                WHERE STR_TO_DATE(Arrive_Time, '%Y-%m-%d %H:%i:%s') < (NOW() - INTERVAL 10 DAY)
            """
            cursor.execute(query)
        return 0
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
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

    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

def get_last_one(airport_code):
    conn = None
    cursor = None
    try:
        # Query di cancellazione specifica
        get_query = """
            SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Arrives 
            WHERE Final_Airport = %s 
            ORDER BY Arrive_Time DESC 
            LIMIT 1
        """
        conn, cursor = connect()  # Usa connect() se non hai 'self'
        cursor.execute(get_query, (airport_code,))
        last_arrival = cursor.fetchone()

        get_query = """
                    SELECT Airport, Arrive_Time, Departure_Time, Final_Airport, Flight_Code FROM Flight_Data_Departures 
                    WHERE Airport = %s 
                    ORDER BY Departure_Time DESC 
                    LIMIT 1
                """
        cursor.execute(get_query, (airport_code,))
        last_departure = cursor.fetchone()  # Restituisce una tupla o None

        return last_arrival, last_departure

    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def get_average_flights(airport_code, days):
    conn = None
    cursor = None
    try:
        conn, cursor = connect()

        # Ci proteggiamo da divisioni per zero
        if int(days) <= 0:
            return 0, 0

        # 1. Conta totale ARRIVI negli ultimi 'days' giorni
        # Final_Airport è dove atterrano
        avg_query = """
            SELECT COUNT(*) FROM Flight_Data_Arrives 
            WHERE Final_Airport = %s 
            AND Arrive_Time >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """
        cursor.execute(avg_query, (airport_code, int(days)))
        total_arrivals = cursor.fetchone()[0]  # fetchone ritorna una tupla (count,)

        # 2. Conta totale PARTENZE negli ultimi 'days' giorni
        # Airport è da dove partono
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
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)

