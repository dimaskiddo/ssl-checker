import smtplib

import config

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from logger import log

def send_email(email_to, subject, body, body_type='plain'):
    if bool(config.EMAIL_SMTP_USE_TLS):
        config.EMAIL_SMTP_PORT = 587

    # Buat objek MIME
    msg = MIMEMultipart()
    msg['From'] = f"{config.EMAIL_FROM} <{config.EMAIL_FROM}>"
    msg['To'] = f"{email_to} <{email_to}>"
    msg['Subject'] = subject

    # Tambahkan isi email ke objek MIME
    msg.attach(MIMEText(body, body_type))

    try:
        # Koneksi ke Gmail SMTP server
        with smtplib.SMTP(config.EMAIL_SMTP_HOST, config.EMAIL_SMTP_PORT) as server:
            if bool(config.EMAIL_SMTP_USE_TLS):
                server.starttls()

            # Login ke akun email
            server.login(config.EMAIL_SMTP_USERNAME, config.EMAIL_SMTP_PASSWORD)

            # Kirim email
            text = msg.as_string()
            server.sendmail(config.EMAIL_FROM, email_to, text)

        return None
    except smtplib.SMTPException as e:
        return f"Unable to send email. {e}"
    except Exception as e:
        return f"Unexpected error. {e}"
