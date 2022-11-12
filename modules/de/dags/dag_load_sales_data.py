from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from tasks.s3_file_download import download_from_s3, rename_file

bucket_name = 'daredata-technical-challenge-data'
local_path = '/var/tmp/'

default_args = {
    'owner': 'Marcus_Waddington',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='load_sales_data',
    default_args=default_args,
    start_date=datetime(2019, 12, 25),
    schedule_interval='@monthly',
    max_active_runs=1,
    tags=["DareData-Challenge"],
    catchup=True
) as dag:

    # dummy start task
    start_task = DummyOperator(task_id="start")

    # transfer sales files from S3
    task_sales_data_download = PythonOperator(
        task_id='sales-data-download',
        python_callable=download_from_s3,
        op_kwargs = {
            'key': 'sales/{{ ds }}/sales.csv',
            'bucket_name': bucket_name,
            'local_path': local_path
        }
    )

    task_sales_data_rename = PythonOperator(
        task_id='sales-data-rename',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'sales-{{ ds }}.csv',
            'download_task_id': 'sales-data-download'
        }
    )

    # transfer store locations from S3 to postgres table
    task_locations_download = PythonOperator(
        task_id='locations-download',
        python_callable=download_from_s3,
        op_kwargs = {
            'key': 'stores.csv',
            'bucket_name': bucket_name,
            'local_path': local_path
        }
    )

    task_locations_rename = PythonOperator(
        task_id='locations-rename',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'stores.csv',
            'download_task_id': 'locations-download'
        }
    )

    #process sales data
    task_sales_postgres = PostgresOperator(
        task_id='sales-append-table',
        postgres_conn_id='postgres_operational_db',
        sql="sql/sales_workflow/sales_table.sql"
    )

    task_locations_postgres = PostgresOperator(
        task_id='locations-create-table',
        postgres_conn_id='postgres_operational_db',
        params = {'path': f"'{local_path}stores.csv'"},
        sql="sql/sales_workflow/store_locations_table.sql"
    )

    task_monthly_sales_postgres = PostgresOperator(
        task_id='monthly-sales-append-table',
        postgres_conn_id='postgres_operational_db',
        sql="sql/sales_workflow/monthly_sales_table.sql"
    )

    start_task >> [
        task_sales_data_download,
        task_locations_download
    ]

    (
        task_sales_data_download
        >> task_sales_data_rename
        >> task_sales_postgres
    )

    (
        task_locations_download
        >> task_locations_rename
        >> task_locations_postgres
    )

    # monthly sales table dependencies
    [
        task_sales_postgres,
        task_locations_postgres
    ] >> task_monthly_sales_postgres