from flask import request
from flask import Flask
import pandas as pd
import psycopg2 as pg
import numpy as np

# set up configuration
host = "localhost"
port = "5432"
database = "postgres"
user = "postgres"
password = "YOUR_PASSWORD"
setting = "dbname=" + database + " user=" + user + " host=" + host + " port=" + port + " password=" + password
engine = pg.connect(setting)

application = Flask(__name__)

@application.route('/ardhani_api/get_total_order', methods=['GET'])
def read():
    content = request.get_json()
    tanggal_mulai = content['tanggal_mulai']
    tanggal_akhir = content['tanggal_akhir']
    query = f"""
                select 
                    count(order_id) as banyaknya_orderan
                from(
                    select 
                        *
                    from(
                        select 
                            distinct on (order_id) order_id
                            , shipping_limit_date 
                        from 
                            items_dataset id 
                        where
                            shipping_limit_date >= '{tanggal_mulai}'
                            and
                            shipping_limit_date < '{tanggal_akhir}'
                        )a
                    order by shipping_limit_date
                )b;
            """
    df = pd.read_sql(query, con=engine)
    result = {
        "banyaknya_orderan": str(df['banyaknya_orderan'].iloc[0])
    }
    print("RESULT", result)
    return result

if __name__ == '__main__':
    application.run(host='0.0.0.0')
