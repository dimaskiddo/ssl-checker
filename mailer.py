import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from logger import log
from utils import parse_env

def send_email(email_to, subject, body):
    # Load credential dan konfigurasi dari environment variable
    email_from = parse_env('EMAIL_FROM')

    # Konfigurasi SMTP server
    smtp_host = parse_env('EMAIL_SMTP_HOST')
    smtp_port = parse_env('EMAIL_SMTP_PORT', 587)
    smtp_user = parse_env("EMAIL_SMTP_USERNAME")
    smtp_pass = parse_env("EMAIL_SMTP_PASSWORD")
    smtp_tls = parse_env('EMAIL_SMTP_USE_TLS', False)

    if bool(smtp_tls):
        smtp_port = 587

    # Buat objek MIME
    msg = MIMEMultipart()
    msg['From'] = f"{email_from} <{email_from}>"
    msg['To'] = f"{email_to} <{email_to}>"
    msg['Subject'] = subject

    # Tambahkan isi email ke objek MIME
    msg.attach(MIMEText(body, 'html'))

    try:
        # Koneksi ke Gmail SMTP server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if bool(smtp_tls):
                server.starttls()

            # Login ke akun email
            server.login(smtp_user, smtp_pass)

            # Kirim email
            text = msg.as_string()
            server.sendmail(email_from, email_to, text)
    except smtplib.SMTPException as e:
        log.error(f"--> Unable to send email: {e}")
    except Exception as e:
        log.error(f"--> Exception when sending mail: {e}")
