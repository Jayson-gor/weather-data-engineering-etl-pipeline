"""
Helper module to run SQL transformations from Airflow.
This uses a direct connection to the database to perform data transformations.
"""
import os
import psycopg2

def run_transformations():
    """
    Run SQL transformations directly using a Python PostgreSQL connection.
    """
    print("Running SQL transformations using direct database connection")
    
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
        
        # Execute SQL for the staging transformation
        print("Running staging transformation...")
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
        
        # Execute SQL for the daily_average transformation
        print("Running daily_average transformation...")
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
        
        # Execute SQL for the weather_report transformation
        print("Running weather_report transformation...")
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
        
        print("All SQL transformations completed successfully!")
        return True
    
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Error running transformations: {e}")
        raise
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    run_transformations()
