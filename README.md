# Big Data E-Commerce Pipeline

## Description
Ce projet implémente un pipeline Big Data complet pour l'analyse en temps réel et par lots des données e-commerce. Il utilise une architecture Lambda moderne combinant Spark Streaming, Kafka, Hadoop, Hive, HBase et Airflow.

## Architecture

![Architecture](docs/architecture_diagram.png)

*   **Ingestion** : Kafka (Topics: clicks, purchases, inventory)
*   **Streaming** : Spark Streaming (Scala) -> HDFS (Parquet) & HBase
*   **Stockage** : HDFS (Data Lake), HBase (NoSQL TR), Hive (Data Warehouse)
*   **Traitement Batch** : Hive / Impala
*   **Orchestration** : Apache Airflow

## Prérequis
*   Docker & Docker Compose
*   Python 3.8+ (pour le generateur)
*   Java 8+ (pour le client Spark local si nécessaire)

## Installation et Démarrage

1.  **Lancer l'infrastructure**
    ```bash
    docker-compose up -d
    ```

2.  **Initialiser HBase**
    ```bash
    docker-compose exec hbase-master /bin/bash /opt/hbase-scripts/create_tables.sh
    ```
    *(Note: le script est monté ou vous pouvez copier-coller les commandes)*

3.  **Lancer le générateur de données**
    ```bash
    cd producer
    pip install -r requirements.txt
    python kafka_producer.py
    ```

4.  **Lancer le Job Spark Streaming**
    *Option 1 (Local SBT)*:
    ```bash
    cd spark-streaming
    sbt run
    ```
    *Option 2 (Submit au cluster)*:
    ```bash
    docker cp spark-streaming/target/scala-2.12/EcommerceStreamProcessor-assembly-1.0.jar spark-master:/tmp/
    docker-compose exec spark-master spark-submit --class com.ecommerce.bigdata.EcommerceStreamProcessor --master spark://spark-master:7077 /tmp/EcommerceStreamProcessor-assembly-1.0.jar
    ```

5.  **Créer les tables Hive**
    ```bash
    docker-compose exec hiveserver2 beeline -u jdbc:hive2://localhost:10000 -n root -f /opt/hive-scripts/create_tables.hql
    ```

6.  **Accéder aux interfaces**
    *   **Airflow** : http://localhost:8080 (admin/admin)
    *   **HDFS NameNode** : http://localhost:9870
    *   **Spark Master** : http://localhost:8080

## Auteurs
*   Hassan BADIR (Superviseur)
*   AL AZAMI

## Licence
Projet académique - 2025
