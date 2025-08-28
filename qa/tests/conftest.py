import os
import sys
import contextlib
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

# Ensure project root is importable (airflow.dags, api_request, etc.)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:14") as pg:
        pg.start()
        os.environ["TEST_PG_HOST"] = pg.get_container_host_ip()
        os.environ["TEST_PG_PORT"] = str(pg.get_exposed_port(5432))
        os.environ["TEST_PG_DB"] = "test_db"
        os.environ["TEST_PG_USER"] = pg.USER
        os.environ["TEST_PG_PASSWORD"] = pg.PASSWORD
        # Create a dedicated test DB
        conn = psycopg2.connect(pg.get_connection_url().replace("postgresql://", "postgres://"))
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT 1 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_db');")
            cur.execute("CREATE DATABASE test_db;")
        conn.close()
        yield pg

@pytest.fixture()
def pg_conn(pg_container):
    dsn = (
        f"dbname={os.environ['TEST_PG_DB']}"
        f" user={os.environ['TEST_PG_USER']}"
        f" password={os.environ['TEST_PG_PASSWORD']}"
        f" host={os.environ['TEST_PG_HOST']}"
        f" port={os.environ['TEST_PG_PORT']}"
    )
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS weather_data;")
    try:
        yield conn
    finally:
        conn.close()
