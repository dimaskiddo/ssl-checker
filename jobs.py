import csv
import datetime

from logger import log
from utils import parse_env, parse_template, fatal_exit

from checker import check_ssl_expiration
from mailer import send_email

def process_csv_file(csv_file_path):
    try:
        # Buka file CSV
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)

            # Baca setiap row file CSV
            for row in reader:
                # Load konfigurasi SSL Checker
                ssl_days_treshold = int(parse_env("SSL_DAYS_TRESHOLD", 30))
                admin_email = parse_env("EMAIL_FROM")

                # Parse baris CSV
                hostname = row['domain'].strip()
                contact_email = row['email'].strip()

                # Cek waktu ekspirasi SSL
                expiration, err = check_ssl_expiration(hostname)

                # Cek apakah cek SSL mengembalikan error
                if err is not None:
                    log.warning(f"{err}")

                    if "Unexpected" in err:
                        log.warning(f"-> Sending Mail Notification to ${admin_email}")

                        body_template = parse_template("templates/errors.html")
                        body_email = body_template.render({"email": admin_email, "hostname": hostname, "error": err})

                        send_email(admin_email, f"Reminder SSL Expiration for \"{hostname}\"", body_email)
                    else:
                        log.warning(f"-> Sending Mail Notification to ${contact_email}")

                        body_template = parse_template("templates/expired.html")
                        body_email = body_template.render({"email": contact_email, "admin": admin_email, "hostname": hostname, "error": err})

                        send_email(contact_email, f"Reminder SSL Expiration for \"{hostname}\"", body_email)
                else:
                    # Menghitung selisih waktu
                    current_date = datetime.datetime.now()
                    days_until_expiration = (expiration - current_date).days

                    if days_until_expiration <= ssl_days_treshold:
                        log.warning(f"\"{hostname}\" Expired at {expiration.strftime('%d-%m-%Y')} ({days_until_expiration} Days from Now)")
                        log.warning(f"-> Sending Mail Notification to {contact_email}")

                        body_template = parse_template("templates/reminder.html")
                        body_email = body_template.render({"email": contact_email, "admin": admin_email, "hostname": hostname, "exp_days": days_until_expiration})

                        send_email(contact_email, f"Reminder SSL Expiration for \"{hostname}\"", body_email)
                    else:
                        log.info(f"\"{hostname}\" Expired at {expiration.strftime('%d-%m-%Y')}")
    except csv.Error:
        fatal_exit(f"Input file is not CSV formated file")
    except StopIteration:
        fatal_exit("CSV file doesn't have correct header")
    except Exception as e:
        fatal_exit(f"Unexpected error. {e}")
