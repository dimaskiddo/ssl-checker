import ssl
import socket
import datetime

from logger import log
from utils import parse_env

def check_ssl_expiration(hostname, port=443):
    try:
        # Membuat socket TCP
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:

            # Mengakses sertifikat SSL menggunakan context
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Mendapatkan informasi sertifikat
                cert = ssock.getpeercert()

                # Mendapatkan tanggal kadaluarsa sertifikat
                expiration_date = cert['notAfter']

        # Mengubah tanggal ke format yang lebih mudah dibaca
        expiration_date = datetime.datetime.strptime(expiration_date, '%b %d %H:%M:%S %Y %Z')
        return expiration_date, None
    except socket.gaierror as e:
        return None, f"\"{hostname}\" Domain Doesn't Have a Record"
    except ssl.SSLError as e:
        return None, f"\"{hostname}\" SSL Certificate is Already Expired or Not Valid"
    except Exception as e:
        return None, f"Unexpected error. {e}"
