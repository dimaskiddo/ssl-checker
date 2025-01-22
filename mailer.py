import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils import parse_env

def send_email(email_to, subject, body):
    # Load credential dan konfigurasi dari environment variable
    email_username = parse_env('EMAIL_USERNAME')
    email_password = parse_env('EMAIL_PASSWORD')

    # Konfigurasi SMTP server
    smtp_host = parse_env('EMAIL_SMTP_HOST')
    smtp_port = parse_env('EMAIL_SMTP_PORT', 587)
    smtp_tls = parse_env('EMAIL_SMTP_USE_TLS', False)

    if bool(smtp_tls):
        smtp_port = 587

    # Buat objek MIME
    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = email_to
    msg['Subject'] = subject

    # Tambahkan isi email ke objek MIME
    msg.attach(MIMEText(body, 'plain'))

    # Koneksi ke Gmail SMTP server
    server = smtplib.SMTP(smtp_host, smtp_port)
    if bool(smtp_tls):
        server.starttls()

    # Login ke akun email
    server.login(email_username, email_password)

    # Kirim email
    text = msg.as_string()
    server.sendmail(email_username, email_to, text)

    # Tutup koneksi
    server.quit()
