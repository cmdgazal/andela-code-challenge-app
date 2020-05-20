import os
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Of course, replace by your correct path
os.environ.update(dotenv)

config = {
    "db_host": os.getenv('db_host'),
    "db_port": int(os.getenv('db_port')),
    "db_name": os.getenv('db_name'),
    "db_user": os.getenv('db_user'),
    "db_pass": os.getenv('db_pass'),
    "crypto_db_table": os.getenv('crypto_db_table'),
    "history_db_table": os.getenv('history_db_table')
}
