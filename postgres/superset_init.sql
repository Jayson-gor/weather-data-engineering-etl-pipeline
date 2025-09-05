CREATE USER superset WITH PASSWORD 'superset';
CREATE DATABASE superset_db OWNER superset;
GRANT ALL PRIVILEGES ON DATABASE superset_db TO superset;

CREATE USER example WITH PASSWORD 'example';
CREATE DATABASE example_db OWNER example;
GRANT ALL PRIVILEGES ON DATABASE example_db TO example;