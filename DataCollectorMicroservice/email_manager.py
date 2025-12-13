import smtplib
import ssl
from email.message import EmailMessage

email = "stiamo.volando2@gmail.com"
my_password = "hndh txfz wicm ehzh"

def make_corpo(email, aircode, condizione):
    corpo = f"Ciao {email}, ti vogliamo avvertire che le tue richieste sui voli relativi all'aeroporto con codice {aircode}, hanno superato la seguente condizione: {condizione}"
    return corpo

def send_email(destinatario, corpo):
    sender_email = email
    password = my_password

    msg = EmailMessage()
    msg.set_content(corpo)
    msg['Subject'] = "LIMITE VOLI SUPERATO"
    msg['From'] = sender_email
    msg['To'] = destinatario
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            return True
    except Exception as e:
        return False