import os
import sys

from jinja2 import Environment, FileSystemLoader

from logger import log

def parse_env(env_name, default=None):
    # Dapatkan value dari environment variable
    env_value = os.getenv(env_name)

    # Cek apakah environment variable ada atau tidak
    if env_value == None:
        # Jika ada default value maka gunakan default value, jika tidak keluarkan error
        if default != None:
            return default
        else:
            log.error(f"{env_name} environment variable is not defined")
            sys.exit(1)
    else:
        # Kembalikan nilai dari environment variable
        return env_value.strip()

def parse_directory_file(path):
    # Mengubah path menjadi format yang benar untuk sistem operasi yang sedang digunakan
    return os.path.normpath(path)

def parse_template(filename):
    # Inisiasi template loader
    template_loader = Environment(loader=FileSystemLoader("./"))
    template_file = parse_directory_file(filename)

    # Cek apakah file template ada
    if os.path.exists(template_file):
        # Kembalikan format template
        return template_loader.get_template(template_file)

    # Jika tidak ada kembalikan None    
    return None

def fatal_exit(message=''):
    # Cek apakah pesan ada isinya
    if len(message.strip()) != 0:
        # Keluarkan pesan dalam bentuk log fatal
        log.fatal(message)

    # Keluar aplikasi dengan exit code 1
    sys.exit(1)
