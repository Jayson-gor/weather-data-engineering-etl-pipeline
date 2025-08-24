from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
import sys

# Add the current directory to Python's path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weather_helpers import main

default_args = {
    'description': 'DAG for orchestrating weather data processing',
    'start_date': datetime(2025, 8, 22),
    'catchup': False,
}

dag = DAG(
    dag_id='weather_api_orchestrator',
    default_args=default_args,
    schedule=timedelta(hours=1),
    catchup=False
)

with dag:
    ingest_task = PythonOperator(
        task_id='ingest_weather_data',
        python_callable=main
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run --project-dir my_project --profiles-dir .',
    )

    # Define the task dependencies
    ingest_task >> dbt_run_task