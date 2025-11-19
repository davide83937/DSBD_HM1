from datetime import datetime

import mysql.connector
from mysql.connector import cursor


class dataManager():
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

   def insertOnDatabase(self, lista):
       insert_query = """
         INSERT INTO Flight_Data (Airport, Flight_code, Final_Airport, Departure_Time, Arrive_Time)
         VALUES (%s, %s, %s, %s, %s)
         """
       conn, cursor =self.connect()
       for flight in lista:
           data = flight.__dict__

           aeroporto = data["estDepartureAirport"]
           codice_volo = data["callsign"].strip()
           aeroporto_finale = data["estArrivalAirport"]
           partenza_ts = data["firstSeen"]
           arrivo_ts = data["lastSeen"]

           # conversione timestamp → datetime
           partenza_dt = datetime.fromtimestamp(partenza_ts)
           arrivo_dt = datetime.fromtimestamp(arrivo_ts)

           cursor.execute(insert_query, (aeroporto, codice_volo, aeroporto_finale, partenza_dt, arrivo_dt))

       conn.commit()
       cursor.close()
       conn.close()



