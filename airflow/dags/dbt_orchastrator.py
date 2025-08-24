from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests
import os

# Define a fetch_data function here instead of importing
def fetch_data(**kwargs):
    print("Fetching weather data...")
    api_key = os.environ.get("WEATHER_API_KEY", "934aed0eebc71a90147fb7b074b4ae01")
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Nairobi"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Data: {data}")
        return data
    except requests.RequestException as e:
        print(f"Error fetching API data: {e}")
        return {"error": str(e)}

default_args = {
    'description': 'DAG for orchestrating dbt models',
    'start_date': datetime(2025, 8, 22),
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='weather_dbt_orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=30),
    max_active_runs=1
)

with dag:
    # Task 1: Fetch weather data
    task1 = PythonOperator(
        task_id='ingest_weather_data',
        python_callable=fetch_data,
    )
    
    # Task 2: Run dbt models directly in the Airflow container
    task2 = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt/my_project && dbt run --profiles-dir=/opt/airflow/dbt'
    )
    
    # Set dependencies
    task1 >> task2