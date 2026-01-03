from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecommerce_daily_analytics',
    default_args=default_args,
    description='Pipeline quotidien E-commerce Big Data',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# 1. Vérifions que des données sont arrivées dans HDFS (via Spark Streaming)
check_data_availability = BashOperator(
    task_id='check_hdfs_data',
    bash_command='hdfs dfs -test -e /data/ecommerce/clicks/event_date={{ ds }}',
    dag=dag,
)

# 2. Réparer les partitions Hive pour découvrir les nouvelles dates
repair_hive_partitions = BashOperator(
    task_id='repair_partitions',
    bash_command='beeline -u jdbc:hive2://hiveserver2:10000 -n root -e "MSCK REPAIR TABLE ecommerce.clicks; MSCK REPAIR TABLE ecommerce.purchases;"',
    dag=dag,
)

# 3. Calculer le revenu quotidien et insérer dans la table agrégée
daily_revenue_aggregation = HiveOperator(
    task_id='daily_revenue_agg',
    hql="""
    INSERT INTO TABLE ecommerce.daily_revenue_by_category
    SELECT 
        '{{ ds }}' as report_date,
        category,
        SUM(total_amount) as total_revenue,
        COUNT(*) as purchase_count,
        AVG(total_amount) as avg_ticket
    FROM ecommerce.purchases
    WHERE event_date = '{{ ds }}'
    GROUP BY category;
    """,
    hive_cli_conn_id='hive_cli_default',
    dag=dag,
)

# 4. Exporter les résultats vers un dossier spécifique pour le Dashboard
export_to_csv = BashOperator(
    task_id='export_stats_csv',
    bash_command="""
    beeline -u jdbc:hive2://hiveserver2:10000 -n root --outputformat=csv2 -e \
    "SELECT * FROM ecommerce.daily_revenue_by_category WHERE report_date='{{ ds }}'" > /opt/airflow/dags/reports/revenue_{{ ds }}.csv
    """,
    dag=dag,
)

# Définition des dépendances
check_data_availability >> repair_hive_partitions >> daily_revenue_aggregation >> export_to_csv
