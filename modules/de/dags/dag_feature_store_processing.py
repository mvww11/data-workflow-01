from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'DareData-Waddington',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='feature_store_processing',
    default_args=default_args,
    start_date=datetime(2022, 6, 29),
    schedule_interval=None,
    max_active_runs=1
) as dag:

    # create feature store
    task_feature_store_postgres = PostgresOperator(
        task_id='feature-store-create-table',
        postgres_conn_id='postgres_operational_db',
        sql="sql/feature_store_workflow/feature_store_table.sql"
    )