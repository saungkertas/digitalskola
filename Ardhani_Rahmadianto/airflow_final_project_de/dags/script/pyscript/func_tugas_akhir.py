import sys
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from airflow.models import Variable

config_MySQL = Variable.get("data_login_mysql",deserialize_json = True)


def get_data_from_api(url_api,ti):
   
    df_json_raw = pd.read_json(url_api)
    df_json = pd.DataFrame(df_json_raw.loc['content']['data'])
    df_for_xcom = df_json.to_json(orient = 'records')
    print("df_for_xcom type : ", type(df_for_xcom))
    ti.xcom_push(key='data_covid_jabar',value=df_for_xcom)

def send_data_MySQL(con_conf,ti):
    data_xcom = ti.xcom_pull(key='data_covid_jabar')#, task_ids = 'get_data_from_api')
    # print("data_xcom type : ", type(data_xcom))
    data_covid_jabar = pd.read_json(data_xcom, orient = 'records')
    # print("data_covid_jabar type : ", type(data_covid_jabar))

    CONNECTION_STRING = f"""mysql+mysqldb://{con_conf["DB_USER"]}:{con_conf["DB_PASSWORD"]}@{con_conf["DB_HOST"]}:{con_conf["DB_PORT"]}/{con_conf["DB_NAME"]}"""
   
    engine = create_engine(CONNECTION_STRING)
    if not database_exists(engine.url):
        create_database(engine.url)

    print("GET DATA API : Connection to MySQL : ",database_exists(engine.url))
    data_covid_jabar.to_sql(name = "staging_area_covid_data", con=engine, if_exists="replace", index=False)
 
def get_from_MySQL_to_Postgres(con_conf_mysql,con_conf_postgres):
    CONNECTION_STRING_MYSQL = f"""mysql+mysqldb://{con_conf_mysql["DB_USER"]}:{con_conf_mysql["DB_PASSWORD"]}@{con_conf_mysql["DB_HOST"]}:{con_conf_mysql["DB_PORT"]}/{con_conf_mysql["DB_NAME"]}"""
    CONNECTION_STRING_POSTGRES = f"""postgresql://{con_conf_postgres["DB_USER"]}:{con_conf_postgres["DB_PASSWORD"]}@{con_conf_postgres["DB_HOST"]}:{con_conf_postgres["DB_PORT"]}/{con_conf_postgres["DB_NAME"]}"""

    engine_mysql = create_engine(CONNECTION_STRING_MYSQL)
    if not database_exists(engine_mysql.url):
        create_database(engine_mysql.url)

    print("Connection to MySQL : ",database_exists(engine_mysql.url))

    engine_postgres = create_engine(CONNECTION_STRING_POSTGRES)
    if not database_exists(engine_postgres.url):
        create_database(engine_postgres.url)

    print("Connection to Postgres : ",database_exists(engine_postgres.url))

    df = pd.read_sql_table("staging_area_covid_data", con=engine_mysql)
    # print("Data Dari MySQL : ", df)
    df.to_sql(name = "data_warehouse", con=engine_postgres, if_exists="replace", index=False)

def create_table_dim_case(con_conf_postgres,ti):
    data_xcom = ti.xcom_pull(key='data_covid_jabar')#, task_ids = 'get_data_from_api')
    # print("data_xcom type : ", type(data_xcom))
    data_covid_jabar = pd.read_json(data_xcom, orient = 'records')
    # algorithm for splitting the status name & details

    temp = data_covid_jabar.columns
    status_name = []
    status_detail = []

    #check for every colum name in dataframe
    for nama_kolom in temp:
        # column name with uppercase letter is the name of status
        if nama_kolom.isupper(): 
            status_name.append(nama_kolom)
        # detail of the status
        else:
            status_detail.append(nama_kolom)

    # splitting the 2 words of status name and detail the save into list
    merge = []
    for word in status_name:
        for sentence in status_detail:
            split = sentence.split("_")
            if word.lower() in split:
                merge.append([split[0].lower(), split[1]])
    dim_case = pd.DataFrame(merge, columns=['status_name','status_detail'])
    
    
    CONNECTION_STRING_POSTGRES = f"""postgresql://{con_conf_postgres["DB_USER"]}:{con_conf_postgres["DB_PASSWORD"]}@{con_conf_postgres["DB_HOST"]}:{con_conf_postgres["DB_PORT"]}/{con_conf_postgres["DB_NAME"]}"""
    engine_postgres = create_engine(CONNECTION_STRING_POSTGRES)
    if not database_exists(engine_postgres.url):
        create_database(engine_postgres.url)

    dim_case.to_sql(name = "temp_dim_case", con=engine_postgres, if_exists="replace", index=False)

# if __name__ == "__main__":
#     url_api = sys.argv[1]
#     # get_data_api_to_db(con_conf)
#     get_data_api_to_mysql(config_MySQL,url_api)