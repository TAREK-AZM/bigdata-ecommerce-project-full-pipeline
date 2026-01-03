-- Create Airflow database
CREATE DATABASE airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE metastore TO bigdata;
GRANT ALL PRIVILEGES ON DATABASE airflow TO bigdata;
