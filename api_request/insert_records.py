from api_request import mock_fetch_data
import psycopg2

def connect_to_database():
    # Simulate a database connection
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host="db",
            dbname="weather_data",
            user="user",
            password="password",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def create_table_if_not_exists(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS weather_data;
                CREATE TABLE IF NOT EXISTS weather_data.weather_data (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100),
                    temperature FLOAT,
                    weather_description TEXT,
                    wind_speed FLOAT,
                    time TIMESTAMP,
                    inserted_at TIMESTAMP DEFAULT NOW(),
                    utc_offset TEXT
                )
            """)
            conn.commit()
            print("Table created successfully or already exists.")
    except psycopg2.Error as e:
        print(f"Failed creating table: {e}")
        conn.rollback()
        raise




def insert_records(conn, data):
    print("Inserting records into the database...")
    try:
        weather = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data.weather_data (city, temperature, weather_description, wind_speed, time, utc_offset)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print("Records inserted successfully.")
    except psycopg2.Error as e:
        print(f"Failed inserting records: {e}")
        conn.rollback()
        raise

def main():
    try:
        conn = connect_to_database()
        create_table_if_not_exists(conn)
        data = mock_fetch_data()
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")


