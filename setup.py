import psycopg2
from config import config

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


def setup_db():
    print("Setting up database............................................")

    conn = create_conn()
    cursor = conn.cursor()
    db_setup = """
    DROP TABLE IF EXISTS {ASSET_TABLE};
    DROP TABLE IF EXISTS {TRADE_TABLE};
    
    CREATE TABLE {ASSET_TABLE} (
        id serial PRIMARY KEY,
        asset_name VARCHAR (64),
        asset_id VARCHAR (64) UNIQUE,
        created_on TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS {TRADE_TABLE} (
        id serial PRIMARY KEY,
        asset_id VARCHAR (64) REFERENCES {ASSET_TABLE}(asset_id),
        time_period_start VARCHAR (64),
        time_period_end VARCHAR (64),
        time_open VARCHAR (64),
        time_close VARCHAR (64),
        price_open NUMERIC (20,10),
        price_high NUMERIC (20,10),
        price_low NUMERIC (20,10),
        price_close NUMERIC (20,10),
        volume_traded NUMERIC (20,10),
        trades_count NUMERIC ,
        created_on TIMESTAMP NOT NULL DEFAULT NOW()
    );
    
    INSERT INTO {ASSET_TABLE} (asset_name, asset_id) VALUES ('Bitcoin', 'BTC');
    INSERT INTO {ASSET_TABLE} (asset_name, asset_id) VALUES ('Ethereum', 'ETH');
    INSERT INTO {ASSET_TABLE} (asset_name, asset_id) VALUES ('Ripple', 'XRP');
    INSERT INTO {ASSET_TABLE} (asset_name, asset_id) VALUES ('Litecoin', 'LTC');
    
    """.format(ASSET_TABLE=crypto_db_table, TRADE_TABLE=history_db_table)

    try:
        cursor.execute(db_setup)
        print("response >>>>>> ", cursor.rowcount)

        print("Tables have been created successfully")

    except Exception as e:
        print("An error occurred ", e)

    conn.commit()
    cursor.close()
    conn.close()


setup_db()
