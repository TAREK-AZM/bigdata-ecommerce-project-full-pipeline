# Rapport Technique : Pipeline Big Data E-Commerce

## 1. Introduction
Dans le cadre du module Big Data / Data Engineering, nous avons conçu et implémenté une architecture complète de traitement de données distribuées. L'objectif est d'analyser en temps réel et en différé les comportements utilisateurs sur une plateforme e-commerce simulée.

## 2. Architecture du Système

Le système repose sur une **Architecture Lambda**, permettant de servir à la fois des vues temps réel (Speed Layer) et des vues historiques précises (Batch Layer).

### 2.1 Composants
1.  **Ingestion (Kafka)** :
    *   Point d'entrée unique pour tous les événements (m découplage producteur/consommateur).
    *   Topics : `ecommerce-clicks`, `ecommerce-purchases`, `ecommerce-inventory`.
    *   Rétention configurée pour 7 jours.

2.  **Traitement Streaming (Spark + Scala)** :
    *   Utilisation de Spark Structured Streaming.
    *   Consommation des topics Kafka.
    *   **Sink HDFS** : Écriture en format Parquet partitionné (`/data/ecommerce/clicks/date=2025-12-25/hour=10/`).
    *   **Sink HBase** : Mise à jour des compteurs temps réel (Revenu par minute).

3.  **Stockage (HDFS & HBase)** :
    *   **HDFS** : Data Lake persistant. Stockage colonnaire (Parquet) pour optimiser les requêtes analytiques.
    *   **HBase** : Accès aléatoire rapide pour l'état des stocks et les profils utilisateurs.

4.  **Traitement Batch & Analytics (Hive & Impala)** :
    *   Tables externes Hive mappées sur les fichiers Parquet HDFS.
    *   Partitionnement dynamique pour performance.
    *   Impala utilisé pour les requêtes ad-hoc à faible latence.

5.  **Orchestration (Airflow)** :
    *   DAG quotidien (`ecommerce_daily_analytics`).
    *   Tâches : Vérification des données -> Réparation des partitions -> Agrégation Revenue -> Export CSV.

## 3. Choix Technologiques

*   **Pourquoi Kafka ?** : Robustesse, débit élevé, persistance des messages.
*   **Pourquoi Spark (Scala) ?** : API riche, typage statique (Scala) évitant les erreurs runtime, performance du moteur in-memory.
*   **Pourquoi Parquet ?** : Compression efficace et "Predicat Pushdown" pour les requêtes SQL (lecture seule des colonnes nécessaires).
*   **Pourquoi Airflow ?** : Gestion fine des dépendances ("Code as Configuration"), interface de monitoring, retries automatiques.

## 4. Implémentation

### 4.1 Générateur de Données
Un script Python simule un trafic réaliste avec des pics d'activité, générant des JSONs structurés envoyés aux brokers Kafka.

### 4.2 Pipeline Spark
```scala
val clicksStream = spark.readStream.format("kafka")...load()
val query = clicksStream.writeStream.format("parquet").partitionBy("event_date")...start()
```
Le code Scala assure la transformation des JSONs bruts en DataFrames typés avant écriture.

### 4.3 Pipeline Airflow
Le DAG Airflow automatise le workflow quotidien. Il utilise `BashOperator` pour les commandes HDFS et ligne de commande, et `HiveOperator` pour les transformations SQL lourdes.

## 5. Cas d'Usage Traités
1.  **Funnel de Conversion** : Analyse du parcours client (Home -> Produit -> Achat).
2.  **Affinités Produits** : Analyse des catégories les plus visitées vs achetées.
3.  **Suivi des Stocks** : Alertes temps réel via HBase sur les niveaux de stock critiques.

## 6. Conclusion
Ce projet a permis de mettre en pratique l'intégration des composants majeurs de l'écosystème Hadoop. L'architecture est scalable horizontalement et tolérante aux pannes grâce à la réplication HDFS et Kafka.
