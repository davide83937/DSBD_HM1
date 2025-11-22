from datetime import datetime
import mysql.connector
from mysql.connector import cursor



# Connessione al database
def connect(self):
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


def insertInterests(self, email, airport_code, mode):
    try:

       insert_query = f"INSERT INTO Interessi (email, airport, mode) VALUES (%s, %s, %s)"
       conn, cursor = self.connect()
       cursor.execute(insert_query, (email, airport_code, mode))
       row = cursor.fetchone()
       if row == None:
           return 0
       else:
           return 1
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)

def insertOnDatabase(self, lista, table):
    try:
       insert_query = f"INSERT INTO {table} (Airport, Flight_code, Final_Airport, Departure_Time, Arrive_Time) VALUES (%s, %s, %s, %s, %s)"
       conn, cursor =self.connect()
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

       conn.commit()

       cursor.close()
       conn.close()
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
           disconnect(conn, cursor)



