from core.constants.env import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD

from email.mime.multipart import MIMEMultipart
import smtplib

def send_email(email:str, assent: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = email
    msg["Subject"] = assent

    with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)