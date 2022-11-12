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
    dag_id='load_client_data',
    default_args=default_args,
    start_date=datetime(2022, 11, 9),
    schedule_interval='@once',
    tags=["DareData-Challenge"]
) as dag:

    # dummy start task
    start_task = DummyOperator(task_id="start")

    # ingest customer_activity.csv from S3
    task_customer_activity_download = PythonOperator(
        task_id='customer-activity-download',
        python_callable=download_from_s3,
        op_kwargs = {
            'key': 'customer_activity.csv',
            'bucket_name': bucket_name,
            'local_path': local_path
        }
    )

    task_customer_activity_rename = PythonOperator(
        task_id='customer-activity-rename',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'customer_activity.csv',
            'download_task_id': 'customer-activity-download'
        }
    )

    # ingest customer_profiles.csv from S3
    task_customer_profiles_download = PythonOperator(
        task_id='customer-profiles-download',
        python_callable=download_from_s3,
        op_kwargs = {
            'key': 'customer_profiles.csv',
            'bucket_name': bucket_name,
            'local_path': local_path
        }
    )

    task_customer_profiles_rename = PythonOperator(
        task_id='customer-profiles-rename',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'customer_profiles.csv',
            'download_task_id': 'customer-profiles-download'
        }
    )

    # ingest labels.csv from S3
    task_labels_download = PythonOperator(
        task_id='labels-download',
        python_callable=download_from_s3,
        op_kwargs = {
            'key': 'labels.csv',
            'bucket_name': bucket_name,
            'local_path': local_path
        }
    )

    task_labels_rename = PythonOperator(
        task_id='labels-rename',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'labels.csv',
            'download_task_id': 'labels-download'
        }
    )

    start_task >> [
        task_customer_activity_download,
        task_customer_profiles_download,
        task_labels_download
    ]

    task_customer_activity_download >> task_customer_activity_rename
    task_customer_profiles_download >> task_customer_profiles_rename
    task_labels_download >> task_labels_rename