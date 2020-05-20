import os
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

config = {
    "db_host": os.getenv('db_host'),
    "db_port": int(os.getenv('db_port')),
    "db_name": os.getenv('db_name'),
    "db_user": os.getenv('db_user'),
    "db_pass": os.getenv('db_pass'),
    "crypto_db_table": os.getenv('crypto_db_table'),
    "history_db_table": os.getenv('history_db_table')
}
