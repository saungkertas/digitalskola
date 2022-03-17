# Insert CSV to database versi menggunakan psycopg2 oleh mas Alan

import pandas as pd
import psycopg2 as pg
import numpy as np
import time as time
import sys


def insert_into_table(conn, df, table):
    """
    Using cursor.mogrify() to build the bulk insert query
    then cursor.execute() to execute the query
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]

    # print("TUPLE" , tuples)
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # print("Banyaknya kolom : ",len(df.columns))
    string_kolom = ("%s," * len(df.columns))[:-1] #generate banyaknya %s, berdasarkan jumlah kolom di df, [:-1] untuk remove last ","
    
    # print(string_kolom)
    # print("COLUMNS", cols)

    # SQL query to execute
    cursor = conn.cursor()
    # values = [cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", tup).decode('utf8') for tup in tuples] 
    values = [cursor.mogrify(f"({string_kolom})", tup).decode('utf8') for tup in tuples] # modular column number
    query = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(values)
    
    # print("QUERY", query)
    try:
        cursor.execute(query, tuples)
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("INSERT DONE")
    cursor.close()

def postgres_import_csv_to_db(host_db,port_db,db_name,user_db,pass_db,csv_file,table_name):
    # set up configuration untuk connect ke DB Postgres
    host = host_db      # "localhost"
    port = port_db      # "5432"
    database = db_name  # "postgres"
    user = user_db      # "postgres"
    password = pass_db  # "YOUR_PASSWORD"
    setting = "dbname=" + database + " user=" + user + " host=" + host + " port=" + port + " password=" + password
    engine = pg.connect(setting)

    # baca data 
    df = pd.read_csv(csv_file) # ('olist_order_items_dataset.csv')
    print(df)

    insert_into_table(engine, df, table_name) # items_dataset

if __name__ == "__main__":
    start = time.time()
    file_csv_location = sys.argv[1]
    table_name_db = sys.argv[2]
    print(file_csv_location)
    postgres_import_csv_to_db("localhost","5432","postgres","postgres","YOUR_PASSWORD",file_csv_location,table_name_db)
    end = time.time()
    print(f'Total waktu proses import csv to db : {round(end-start,5)} second')

# Cara panggil program dengan argument lokasi file csv dan table name di db 
# contoh : python3 csv_insert_to_db.py olist_order_items_dataset.csv items_dataset