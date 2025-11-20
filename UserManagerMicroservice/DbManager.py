import mysql.connector
from mysql.connector import cursor


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


def login(email, password):
    conn = None
    cursor = None
    try:
       login_query = f"SELECT * FROM Users WHERE email = '{email}' AND password = '{password}'"
       conn, cursor = connect()
       cursor.execute(login_query)
       n = cursor.rowcount
       return check_n(n)
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



