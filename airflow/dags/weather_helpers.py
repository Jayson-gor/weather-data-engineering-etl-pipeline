import psycopg2
import requests

def fetch_data(city="Nairobi"):
    print(f"Fetching weather data for {city} from API...")
    # Get API key from environment variable
    import os
    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key:
        print("Warning: WEATHER_API_KEY environment variable not found. Using fallback method.")
        api_key = "934aed0eebc71a90147fb7b074b4ae01"  # Fallback for development only
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city},Kenya"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        print(f"Status Code: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching API data for {city}: {e}")
        return {"error": str(e), "city": city}

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
        
        # List of major towns in Kenya
        kenya_towns = [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", 
            "Nyeri", "Kakamega", "Thika", "Garissa", "Kitale", 
            "Kiambu", "Lamu"
        ]
        
        # Fetch and insert data for each town
        success_count = 0
        for town in kenya_towns:
            print(f"Processing {town}...")
            data = fetch_data(town)
            
            # Check if there was an error fetching data
            if "error" in data:
                print(f"Cannot proceed with ingestion for {town} due to API error: {data['error']}")
                continue
                
            insert_records(conn, data)
            success_count += 1
            
        print(f"Successfully processed {success_count} out of {len(kenya_towns)} towns")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")
