"""
Helper module to run dbt models from Airflow.
This uses a direct connection to the database instead of the Docker exec approach.
"""
import os
import subprocess
import tempfile
from pathlib import Path
import psycopg2
from jinja2 import Template

def run_dbt_models():
    """
    Run dbt models directly using a Python PostgreSQL connection.
    This bypasses the need to use Docker commands.
    """
    print("Running dbt models using direct database connection")
    
    # Database connection parameters (from environment variables)
    conn_params = {
        'host': 'db',
        'dbname': os.environ.get('POSTGRES_DB', 'weather_data'),
        'user': os.environ.get('POSTGRES_USER', 'user'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'port': 5432
    }
    
    print(f"Connecting to database: {conn_params['dbname']} as {conn_params['user']}")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Execute SQL for the staging model
        print("Running staging model...")
        staging_sql = """
        CREATE SCHEMA IF NOT EXISTS weather_data;
        
        DROP TABLE IF EXISTS weather_data.staging;
        
        CREATE TABLE weather_data.staging AS
        SELECT 
            city,
            temperature,
            weather_description,
            wind_speed,
            time,
            inserted_at,
            utc_offset
        FROM weather_data.weather_data;
        """
        cursor.execute(staging_sql)
        conn.commit()
        
        # Execute SQL for the daily_average model
        print("Running daily_average model...")
        daily_avg_sql = """
        CREATE SCHEMA IF NOT EXISTS weather_data;
        
        DROP TABLE IF EXISTS weather_data.daily_average;
        
        CREATE TABLE weather_data.daily_average AS
        SELECT 
            city,
            DATE(time) as day,
            AVG(temperature) as avg_temperature,
            AVG(wind_speed) as avg_wind_speed,
            COUNT(*) as observation_count
        FROM weather_data.staging
        GROUP BY city, DATE(time);
        """
        cursor.execute(daily_avg_sql)
        conn.commit()
        
        # Execute SQL for the weather_report model
        print("Running weather_report model...")
        weather_report_sql = """
        CREATE SCHEMA IF NOT EXISTS weather_data;
        
        DROP TABLE IF EXISTS weather_data.weather_report;
        
        CREATE TABLE weather_data.weather_report AS
        SELECT 
            s.city,
            s.time,
            s.temperature,
            s.weather_description,
            s.wind_speed,
            da.avg_temperature,
            s.temperature - da.avg_temperature as temp_diff_from_daily_avg
        FROM weather_data.staging s
        JOIN weather_data.daily_average da 
            ON s.city = da.city 
            AND DATE(s.time) = da.day;
        """
        cursor.execute(weather_report_sql)
        conn.commit()
        
        print("All dbt models completed successfully!")
        return True
    
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Error running dbt models: {e}")
        raise
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    run_dbt_models()
