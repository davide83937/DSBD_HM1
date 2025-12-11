import smtplib
import ssl
from email.message import EmailMessage

email = "davidepanto@gmail.com"
my_password = "rwqi sycq dolj bllf"

def make_corpo(email, aircode, condizione):
    corpo = f"Ciao {email}, ti vogliamo avvertire che le tue richieste sui voli relativi all'aeroporto con codice {aircode}, hanno superato la seguente condizione: {condizione}"
    return corpo

def send_email(destinatario, corpo):
    # Configurazione Sender (la tua mail)
    sender_email = email
    # ATTENZIONE: Qui va la 'App Password' di Google, non la tua password normale!
    password = my_password

    msg = EmailMessage()
    msg.set_content(corpo)  # Contenuto del messaggio
    msg['Subject'] = "Limite voli superato"
    msg['From'] = sender_email
    msg['To'] = destinatario

    # Connessione al server SMTP di Gmail
    context = ssl.create_default_context()

    try:
        # Usa la porta 465 per SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Email inviata a {destinatario}")
            return True
    except Exception as e:
        print(f"Errore invio email: {e}")
        return False