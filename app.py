from flask import Flask, request, json, Response
from config import config
import psycopg2
import json
import decimal
import sys

db_host = config["db_host"]
db_port = config["db_port"]
db_name = config["db_name"]
db_user = config["db_user"]
db_pass = config["db_pass"]
crypto_db_table = config["crypto_db_table"]
history_db_table = config["history_db_table"]


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


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
        sys.exit(1)
    return conn


app = Flask(__name__)
conn = create_conn()


@app.route('/get_historical_data', methods=['GET'])
def create_dag():
    asset_id = request.args.get('asset_id')
    print("Asset ID ", asset_id)
    if asset_id:
        cursor = conn.cursor()
        cursor.execute(
            "with query_res as (select A.*, B.asset_name from trades A left join assets B on A.asset_id = B.asset_id where A.asset_id = '{ASSET}') select json_agg(query_res) from query_res".format(ASSET=asset_id))
        result = cursor.fetchall()
        rowcount = cursor.rowcount
        if rowcount >= 1:
            conn.commit()
            cursor.close()
            return Response(
                mimetype="application/json",
                response=json.dumps({'err': False, 'msg': 'records found', 'data': result[0][0]}),
                status=200
            )
        else:
            conn.commit()
            cursor.close()
            return Response(
                mimetype="application/json",
                response=json.dumps({'err': True, 'msg': 'no records found', 'data': []}),
                status=404
            )
    else:
        return Response(
            mimetype="application/json",
            response=json.dumps({'err': True, 'msg': 'No asset id found in your request'}),
            status=200
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
