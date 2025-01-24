import env
import sys
import csv
import datetime

from logger import log
from utils import parse_template

from checker import check_ssl_expiration
from mailer import send_email

def process_csv_file(csv_file_path):
    try:
        # Buka file CSV
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)

            # Baca setiap row file CSV
            for row in reader:
                # Parse baris CSV
                hostname = row['domain'].strip()
                contact_email = row['email'].strip()

                # Cek waktu ekspirasi SSL
                expiration, err = check_ssl_expiration(hostname)

                # Cek apakah cek SSL mengembalikan error
                if err is not None:
                    log.warning(f"{err}")

                    if "Unexpected" in err:
                        log.warning(f"-> Sending Mail Notification to ${env.EMAIL_FROM}")

                        body_template = parse_template("templates/errors.html")
                        body_email = body_template.render({"email": env.EMAIL_FROM, "hostname": hostname, "error": err})

                        err = send_email(env.EMAIL_FROM, f"Galat Pengecekan Kedaluwarsa SSL untuk \"{hostname}\"", body_email, 'html')
                        if err is not None:
                            log.error(f"--> {err}")
                    else:
                        log.warning(f"-> Sending Mail Notification to ${contact_email}")

                        body_template = parse_template("templates/expired.html")
                        body_email = body_template.render({"email": contact_email, "admin": env.EMAIL_FROM, "hostname": hostname, "error": err})

                        err = send_email(contact_email, f"Peringatan Kedaluwarsa SSL untuk \"{hostname}\"", body_email, 'html')
                        if err is not None:
                            log.error(f"--> {err}")
                else:
                    # Menghitung selisih waktu
                    current_date = datetime.datetime.now()
                    days_until_expiration = (expiration - current_date).days

                    if days_until_expiration <= env.SSL_DAYS_TRESHOLD:
                        log.warning(f"\"{hostname}\" Expired at {expiration.strftime('%d-%m-%Y')} ({days_until_expiration} Days from Now)")
                        log.warning(f"-> Sending Mail Notification to {contact_email}")

                        body_template = parse_template("templates/reminder.html")
                        body_email = body_template.render({"email": contact_email, "admin": env.EMAIL_FROM, "hostname": hostname, "exp_days": days_until_expiration})

                        err = send_email(contact_email, f"Pengingat Kedaluwarsa SSL untuk \"{hostname}\"", body_email, 'html')
                        if err is not None:
                            log.error(f"--> {err}")
                    else:
                        log.info(f"\"{hostname}\" Expired at {expiration.strftime('%d-%m-%Y')}")
    except csv.Error:
        log.fatal(f"Input file is not CSV formated file")
        sys.exit(1)
    except StopIteration:
        log.fatal("CSV file doesn't have correct header")
        sys.exit(1)
    except Exception as e:
        log.fatal(f"Unexpected error. {e}")
        sys.exit(1)
