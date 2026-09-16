from core.constants.env import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD
from core.constants.paths import USER_FILES_FOLDER_PATH

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import os

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx"
}

def send_email(email:str, subject: str, body: str):
    msg = MIMEMultipart()

    msg["From"] = SMTP_USER
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    if os.path.exists(USER_FILES_FOLDER_PATH):
        for filename in os.listdir(USER_FILES_FOLDER_PATH):
            file_path = os.path.join(USER_FILES_FOLDER_PATH, filename)
            extension = os.path.splitext(filename)[1].lower()

            if not os.path.isfile(file_path):
                continue

            if extension not in ALLOWED_EXTENSIONS:
                continue

            with open(file_path, "rb") as file:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(file.read())

            encoders.encode_base64(attachment)

            attachment.add_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )

            msg.attach(attachment)

    with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)