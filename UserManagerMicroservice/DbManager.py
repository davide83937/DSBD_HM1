import mysql.connector
from mysql.connector import cursor
import random
import string


def connect():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="anto",
        password="onta",
        database="UserDB"
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

def check_user(email):
    try:
       check_query = f"SELECT * FROM Users WHERE email = '{email}'"
       conn, cursor = connect()
       cursor.execute(check_query)
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


def check_n(n):
  if n == 1:
     return 0
  else:
    return 1


def cancellazione_sessione(email):
    conn = None
    cursor = None
    try:
        query = "DELETE FROM Logged_Users WHERE email = %s"
        conn, cursor = connect()
        cursor.execute(query, (email,))
        n = cursor.rowcount
        return check_n(n)
    except mysql.connector.DatabaseError as e:
         print("Errore generico del database:", e)
         return -1
    finally:
         if conn != None:
             disconnect(conn, cursor)


def check_logging(email):
    conn = None
    cursor = None
    try:
        check_login_query = "SELECT * FROM Logged_Users WHERE email = %s"
        conn, cursor = connect()
        cursor.execute(check_login_query, (email,))
        n = cursor.rowcount
        return check_n(n)
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)


def login(email, password, first):
    conn = None
    cursor = None
    try:
        if first == True:
            if check_logging(email) == 0:
               return 2
        login_query = "SELECT * FROM Users WHERE email = %s AND password = %s"
        conn, cursor = connect()
        cursor.execute(login_query, (email, password))
        n = cursor.rowcount
        response = check_n(n)
        if first == True:
            if response == 0:
                insert_session_id_query = "INSERT INTO Logged_Users (email, id_session) VALUES (%s, %s)"
                length = 20
                session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
                cursor.execute(insert_session_id_query, (email,session_id))
                n = cursor.rowcount
                return check_n(n)
        else:
            return response
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
          disconnect(conn, cursor)


def registrazione(email, username, password):
    conn = None
    cursor = None
    try:
      registration_query = f"INSERT INTO Users (email, username, password) VALUES (%s, %s, %s)"
      conn, cursor = connect()
      cursor.execute(registration_query, (email, username, password))
      n = cursor.rowcount
      return check_n(n)
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
          disconnect(conn, cursor)


def cancellazione(email):
    conn = None
    cursor = None
    try:
       delete_query = "DELETE FROM Users WHERE email = %s"
       conn, cursor = connect()
       cursor.execute(delete_query, (email,))
       n = cursor.rowcount
       return check_n(n)
    except mysql.connector.DatabaseError as e:
        print("Errore generico del database:", e)
        return -1
    finally:
        if conn != None:
            disconnect(conn, cursor)



