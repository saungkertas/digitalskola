# Insert CSV to database versi menggunakan sqlAlchemy oleh mas Bagas

import pandas as pd
import time as time
from sqlalchemy import create_engine
import logging

start = time.time()
logging.basicConfig(level=logging.INFO)

def write_to_postgres(df, db_name, table_name, connection_string):
    engine = create_engine(connection_string)
    logging.info(f"Writing dataframe to database: '{db_name}', table: '{table_name}' ...")
    df.to_sql(name = table_name, con=engine, if_exists="replace", index=False)

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "YOUR_PASSWORD"
DB_HOST = "localhost"
DB_PORT = "5432"
CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
TABLE_NAME = "items_dataset"

print(CONNECTION_STRING)

df_csv = pd.read_csv('olist_order_items_dataset.csv')
print(df_csv)

write_to_postgres(df=df_csv, db_name=DB_NAME, table_name=TABLE_NAME, connection_string=CONNECTION_STRING)

end = time.time()
print(f'Total waktu proses import csv to db : {round(end-start,5)} second')
