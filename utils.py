import os
import sys

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

def fatal_exit(message=''):
    if len(message.strip()) != 0:
        log.fatal(message)

    sys.exit(1)
