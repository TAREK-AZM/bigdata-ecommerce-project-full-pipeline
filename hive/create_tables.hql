-- Création de la base de données
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Table externe pour les CLICS (format Parquet généré par Spark partitionné)
CREATE EXTERNAL TABLE IF NOT EXISTS clicks (
  event_id STRING,
  user_id STRING,
  product_id STRING,
  category STRING,
  page_url STRING,
  timestamp BIGINT,
  session_id STRING,
  device STRING
)
PARTITIONED BY (event_date STRING, event_hour INT)
STORED AS PARQUET
LOCATION '/data/ecommerce/clicks';

-- Récupération des partitions (à exécuter régulièrement)
MSCK REPAIR TABLE clicks;

-- Table externe pour les ACHATS (format Parquet)
CREATE EXTERNAL TABLE IF NOT EXISTS purchases (
  transaction_id STRING,
  user_id STRING,
  product_id STRING,
  category STRING,
  quantity INT,
  unit_price DOUBLE,
  total_amount DOUBLE,
  payment_method STRING,
  timestamp BIGINT,
  status STRING
)
PARTITIONED BY (event_date STRING, event_hour INT)
STORED AS PARQUET
LOCATION '/data/ecommerce/purchases';

-- Récupération des partitions
MSCK REPAIR TABLE purchases;

-- Table agrégée : Revenu quotidien par catégorie
CREATE TABLE IF NOT EXISTS daily_revenue_by_category (
  report_date STRING,
  category STRING,
  total_revenue DOUBLE,
  purchase_count INT,
  avg_ticket DOUBLE
)
STORED AS PARQUET;
