import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings


class EmailService:
    def __init__(self):
        self.__sender_email = settings.SMTP_USER
        self.__sender_password = settings.SMTP_PASSWORD
        self.tls = settings.SMTP_TLS
        self.__port = settings.SMTP_PORT
        self.__host = settings.SMTP_HOST

    def send_email(self, html_content: str, email: str, subject: str):
        msg = MIMEMultipart()
        msg["From"] = self.__sender_email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        # Attach the Stori logo to the email
        with open("static/img/stori_logo.svg", "rb") as logo_file:
            logo_data = logo_file.read()
            logo_part = MIMEImage(logo_data, _subtype="svg+xml")
            logo_part.add_header("Content-ID", "<stori_logo>")
            msg.attach(logo_part)

        with smtplib.SMTP_SSL(self.__host, self.__port) as server:
            server.login(self.__sender_email, self.__sender_password)
            server.sendmail(self.__sender_email, email, msg.as_string())
