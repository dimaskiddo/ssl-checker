#!/usr/bin/env python3

import os
import sys
import time
import schedule

from logger import log
from utils import fatal_exit
from dotenv import load_dotenv
from jobs import process_csv_file

if __name__ == "__main__":
    # Dapatkan nama script yang di jalankan
    script_name = os.path.basename(__file__)

    # Cek apakah parameter file CSV di inputkan
    if len(sys.argv) != 2:
        fatal_exit(f"Usage: python3 {script_name} <path_to_csv_file>")
 
    # Load konfigurasi dari .env
    load_dotenv()

    # Mengambil path file CSV dari inputan script
    csv_file_path = sys.argv[1]

    # Masukan pengecekan SSL Domain sebagai shceduled job
    schedule.every().minutes.do(process_csv_file, csv_file_path)

    # Loop untuk menjalankan scheduled job
    while True:
        schedule.run_pending()
        time.sleep(1)
