from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable

from script.pyscript import func_tugas_akhir

config_MySQL = Variable.get("data_login_mysql",deserialize_json = True)
config_Postgres = Variable.get("data_login_postgres",deserialize_json = True)

with DAG(
    dag_id='dag_tugas_akhir_de',
    schedule_interval='@daily',
    start_date=datetime(2022,4,25),
    catchup= False 
) as dag:
    get_data_from_api = PythonOperator(
        task_id = 'get_data_from_api',
        python_callable = func_tugas_akhir.get_data_from_api,
        op_kwargs = {"con_conf" : config_MySQL , "url_api" : 'https://covid19-public.digitalservice.id/api/v1/rekapitulasi_v2/jabar/harian?level=kab'}
    )

    send_data_to_MySQL = PythonOperator(
        task_id = 'send_data_to_MySQL',
        python_callable = func_tugas_akhir.send_data_MySQL,
        op_kwargs = {"con_conf" : config_MySQL , "url_api" : 'https://covid19-public.digitalservice.id/api/v1/rekapitulasi_v2/jabar/harian?level=kab'}
    )

    get_from_MySQL_to_Postgres = PythonOperator(
        task_id = 'get_from_MySQL_to_Postgres',
        python_callable = func_tugas_akhir.get_from_MySQL_to_Postgres,
        op_kwargs = {"con_conf_mysql" : config_MySQL,"con_conf_postgres" : config_Postgres}
    )

    create_table_postgres = PostgresOperator(
        task_id="create_table_postgres",
        postgres_conn_id="postgres_tugas_akhir_de",
        sql="script/sqlscript/create_table_postgres.sql"
    )

    create_table_dim_case = PythonOperator(
        task_id = 'create_table_dim_case',
        python_callable = func_tugas_akhir.create_table_dim_case,
        op_kwargs = {"con_conf_postgres" : config_Postgres}
    )

    insert_aggregate_dim_fact = PostgresOperator(
        task_id="insert_aggregate_dim_fact",
        postgres_conn_id="postgres_tugas_akhir_de",
        sql="script/sqlscript/agg_insert_data_dim_fact.sql"
    )

get_data_from_api >> send_data_to_MySQL >> get_from_MySQL_to_Postgres >> create_table_postgres >> create_table_dim_case >> insert_aggregate_dim_fact