import os

from jinja2 import Environment, FileSystemLoader

from logger import log

def parse_env(env_name, default=None, empty_fatal=None):
    # Dapatkan value dari environment variable
    env_value = os.getenv(env_name)

    # Cek apakah environment variable ada atau tidak
    if env_value == None:
        # Jika ada default value maka gunakan default value, jika tidak keluarkan error
        if default != None:
            return default
        else:
            # Jika tidak ada value dan empty_fatal tidak none maka keluarkan pesan fatal
            if empty_fatal is not None:
                fatal_exit(f"{env_name} environment variable is not defined")
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
