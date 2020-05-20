import requests
import argparse
import sys
from datetime import date
from config import config
import psycopg2

db_host = config["db_host"]
db_port = config["db_port"]
db_name = config["db_name"]
db_user = config["db_user"]
db_pass = config["db_pass"]
crypto_db_table = config["crypto_db_table"]
history_db_table = config["history_db_table"]


def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(user=db_user,
                                password=db_pass,
                                host=db_host,
                                port=db_port,
                                database=db_name)

        print('connected')
    except Exception as e:
        print("Cannot connect.")
        print(e)
    return conn


def get_number_of_days():
    return str((date.today() - date(2016, 1, 1)).days)


def write_to_db(records, asset_id):
    conn = create_conn()
    cursor = conn.cursor()

    for rec in records:
        insert_query = (
            "INSERT INTO {TABLE} (asset_id, time_period_start, time_period_end, time_open, time_close, price_open, price_high, price_low, price_close, volume_traded, trades_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(
                TABLE=history_db_table))
        insert_values = (asset_id,
                         rec["time_period_start"], rec["time_period_end"], rec["time_open"], rec["time_close"],
                         rec["price_open"], rec["price_high"], rec["price_low"], rec["price_close"],
                         rec["volume_traded"], rec["trades_count"])
        cursor.execute(insert_query, insert_values)

    conn.commit()
    cursor.close()
    conn.close()


allowed_cryptos = ["BTC", "ETH", "XRP", "LTC"]

# Define the program description
text = 'This is a coinapi.co crypto fetcher'

# Initiate the parser with a description
parser = argparse.ArgumentParser(description=text, allow_abbrev=False)

parser.add_argument("--apikey", action='store', type=str, required=True, help="your api key")
parser.add_argument("--crypto", action='store', type=str, required=True,
                    help="cryptocurrency asset id: BTC, ETH, XRP, LTC")

args = parser.parse_args()

crypto_id = args.crypto
apikey = args.apikey

if str(crypto_id).upper() not in allowed_cryptos:
    print('This crypto is not allowed currently')
    sys.exit()

url = 'https://rest.coinapi.io/v1/ohlcv/{ASSET}/USD/history?period_id=1DAY&time_start=2016-01-01T00:00:00&limit={limit}'.format(
    ASSET=str(crypto_id).upper(), limit=int(get_number_of_days()))
headers = {'X-CoinAPI-Key': apikey}
response = requests.get(url, headers=headers)

try:
    write_to_db(response.json(), str(crypto_id).upper())
    print("Data has been written to database successfully")
except Exception as e:
    print("An error occurred ", e)
