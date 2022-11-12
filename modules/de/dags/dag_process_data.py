from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator

local_path = '/var/tmp/'

default_args = {
    'owner': 'Marcus_Waddington',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='process_data',
    default_args=default_args,
    start_date=datetime(2022, 6, 29),
    schedule_interval=None,
    max_active_runs=1,
    tags=["DareData-Challenge"]
) as dag:

    # dummy start task
    start_task = DummyOperator(task_id="start")

    #process customers data
    task_customer_activity_postgres = PostgresOperator(
        task_id='customer-activity-create-table',
        postgres_conn_id='postgres_operational_db',
        params = {'path': f"'{local_path}customer_activity.csv'"},
        sql="sql/customers_workflow/customer_activity_table.sql"
    )

    task_customer_profiles_postgres = PostgresOperator(
        task_id='customer-profiles-create-table',
        postgres_conn_id='postgres_operational_db',
        params = {'path': f"'{local_path}customer_profiles.csv'"},
        sql="sql/customers_workflow/customer_profiles_table.sql"
    )

    task_labels_postgres = PostgresOperator(
        task_id='labels-create-table',
        postgres_conn_id='postgres_operational_db',
        params = {'path': f"'{local_path}labels.csv'"},
        sql="sql/customers_workflow/labels_table.sql"
    )



    #process feature store
    task_feature_store_postgres = PostgresOperator(
        task_id='feature-store-create-table',
        postgres_conn_id='postgres_operational_db',
        sql="sql/feature_store_workflow/feature_store_table.sql"
    )

    # declare task dependencies
    start_task >> [
        task_customer_activity_postgres,
        task_customer_profiles_postgres,
        task_labels_postgres
    ]

    # feature store dependencies
    [
        task_customer_activity_postgres,
        task_customer_profiles_postgres,
        task_labels_postgres
    ] >> task_feature_store_postgres