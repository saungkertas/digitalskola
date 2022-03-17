import pandas as pd
import psycopg2 as pg
import numpy as np
import time as time
import sys

def read_tableDB_to_df(engine,table_name):
    query = f"""
        select
            *
        from
            {table_name}
        """
    # print(query)
    df_read = pd.read_sql(query, con=engine)
    return df_read

def db_connection(host_db,port_db,db_name,user_db,pass_db):
    # set up configuration untuk connect ke DB Postgres
    host = host_db      # "localhost"
    port = port_db      # "5432"
    database = db_name  # "postgres"
    user = user_db      # "postgres"
    password = pass_db  # "YOUR PASSWORD"
    setting = "dbname=" + database + " user=" + user + " host=" + host + " port=" + port + " password=" + password
    engine = pg.connect(setting)
    return engine

if __name__ == "__main__":
    start = time.time()
    table_name_db = sys.argv[1]

    engineDB = db_connection("localhost","5432","postgres","postgres","YOUR_PASSWORD")
    df_from_tableDB = read_tableDB_to_df(engineDB,table_name_db) # "items_dataset"
    print(df_from_tableDB)
    
    end = time.time()
    print(f'Total waktu proses read db_table to DF : {round(end-start,5)} second')
