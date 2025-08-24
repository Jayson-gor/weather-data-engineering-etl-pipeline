# Weather Data Project

This project collects weather data for major towns in Kenya and stores it in a PostgreSQL database using Apache Airflow for orchestration.

## Project Structure

```
data_modelling/
  └── weather_data_project/
      ├── airflow/
      │   └── dags/             # Airflow DAG files
      ├── api_request/          # API request modules
      ├── postgres/             # PostgreSQL initialization scripts
      │   └── data/             # PostgreSQL data (gitignored)
      ├── .env                  # Environment variables (gitignored)
      ├── .gitignore            # Git ignore file
      ├── docker-compose.yaml   # Docker Compose configuration
      └── readme.md             # This file
```

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Git

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather_data_project.git
   cd weather_data_project
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and replace all placeholder values with secure credentials:
   - Generate strong passwords (min 16 characters)
   - Use a real email address for pgAdmin
   - Get your actual WeatherStack API key
   - Generate secure secret keys (32+ characters)

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the services:
   - Airflow: http://localhost:8000 (use credentials from .env file)
   - Superset: http://localhost:8088 (use credentials from .env file)
   - pgAdmin: http://localhost:5050 (use credentials from .env file)

## Production Deployment Checklist

### Security Requirements
- [ ] Replace all default passwords with strong credentials
- [ ] Set up proper SSL/TLS certificates
- [ ] Configure firewall rules (only allow necessary ports)
- [ ] Use secrets management (HashiCorp Vault, AWS Secrets Manager)
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Enable audit logging

### Production Environment
- [ ] Use production-grade database (managed PostgreSQL)
- [ ] Set up load balancers
- [ ] Configure auto-scaling
- [ ] Set up CI/CD pipelines
- [ ] Use container orchestration (Kubernetes)
- [ ] Implement disaster recovery
- [ ] Set up monitoring (Prometheus, Grafana)

### Current Status: ⚠️ **DEVELOPMENT ONLY**
This setup is currently suitable for development and testing only. Do not deploy to production without implementing the security checklist above.

## Setting up pgAdmin Connection

1. Open pgAdmin at http://localhost:5050
2. Login with the credentials from your `.env` file
3. Right-click on "Servers" and select "Create > Server"
4. In the "General" tab, name your connection (e.g., "Weather Database")
5. In the "Connection" tab, enter:
   - Host: db
   - Port: 5432
   - Database: weather_data
   - Username: user
   - Password: password (from .env)
6. Click "Save"

## Important Notes

- The `.env` file contains sensitive information and is excluded from git. Make sure to keep it secure and never commit it to the repository.
- If you plan to deploy this project, make sure to set up proper security measures for your database and API keys.

## Technology Stack

- Apache Airflow: Workflow orchestration
- PostgreSQL: Database
- pgAdmin: Database management UI
- WeatherStack API: Weather data source
- Docker & Docker Compose: Containerization

## notes on .gitignore
The .gitignore file is essential for Git version control because:

Excludes sensitive information: It prevents sensitive data like API keys, passwords, and credentials (in your .env file) from being committed to your repository, which helps protect your security.

Reduces repository size: It excludes large or unnecessary files (like PostgreSQL data files) that don't need to be tracked, keeping your repository small and efficient.

Excludes temporary files: It prevents temporary files, build artifacts, and cache files (like __pycache__ folders and .pyc files) from cluttering your repository.

Prevents environment-specific files: It excludes files that are specific to your local development environment that other developers don't need.

Improves collaboration: It ensures that team members only commit relevant source code and documentation, not their personal settings or environment-specific files.

In your specific project, the .gitignore file is essential for:

Keeping your WeatherStack API key private by excluding the .env file
Excluding database data files (which can be quite large and are regenerated on each system)
Excluding Python cache files that are automatically generated and don't need tracking
Excluding log files that are generated during runtime

## dbt
13:26:56  Setting up your profile.
Which database would you like to use?
[1] postgres

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 1
host (hostname for the instance): db
port [5432]: 5432
user (dev username): user
pass (dev password): 
dbname (default database that dbt will build objects in): db
schema (default schema that dbt will build objects in): dev
threads (1 or more) [1]: 4


## dbt orchastrator
✅ What's Working:
Volume Mounting: The dbt project is properly mounted from ./dbt:/opt/airflow/dbt in the Airflow container
dbt Installation: dbt-postgres is installed and available in the Airflow container
Task Execution:
ingest_weather_data task successfully fetches data (handles API rate limits gracefully)
run_dbt_models task successfully runs all 3 dbt models:
staging (11 records processed)
daily_average (8 records processed)
weather_report (11 records processed)
Task Dependencies: Proper sequencing with task1 >> task2
dbt Profiles: Using the correct profiles directory (--profiles-dir=/opt/airflow/dbt)
🔧 Key Technical Solutions:
BashOperator: Running dbt directly in the Airflow container instead of Docker exec (avoiding socket permission issues)
Volume Management: Proper mounting ensures dbt project files are accessible
Path Configuration: Using absolute paths (/opt/airflow/dbt/my_project) for reliable execution
Error Handling: Graceful handling of API rate limits and proper error reporting
📊 Current Status:
My weather data pipeline is now orchestrating:

Data Ingestion: Fetching weather data from the API
Data Transformation: Running dbt models to process and transform the data
Scheduling: Ready to run every 30 minutes as configured
The pipeline successfully ran all dbt transformations with PASS=3 WARN=0 ERROR=0, demonstrating that your dbt models are working correctly with the existing data in your PostgreSQL database.


## summary
1. docker-compose.yaml - Full setup with all services (db, pgadmin, airflow, dbt, superset)
2. docker-compose-simple.yaml - Minimal backup without Superset
My weather data pipeline is now running with:

✅ Airflow for orchestration
✅ dbt for transformations
✅ Postgres for data storage
✅ Superset for BI with examples loaded
✅ pgAdmin for database management
And you can access:

Airflow UI: http://localhost:8080 (admin/admin)
Superset UI: http://localhost:8088 (admin/admin)
pgAdmin: http://localhost:5050