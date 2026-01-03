# Présentation du Projet Big Data

## Slide 1 : Titre
**Plateforme d'Analyse E-Commerce Big Data**
*Sous-titre : Ingestion, Traitement et Visualisation Distribués*
*Présenté par : AL AZAMI*

---

## Slide 2 : Objectifs
*   Construire un pipeline de données complet (End-to-End).
*   Maîtriser l'écosystème Hadoop (HDFS, Hive, HBase).
*   Implémenter un traitement temps réel avec Spark & Kafka.
*   Orchestrer les flux avec Airflow.

---

## Slide 3 : Architecture Globale
*(Schéma Architecture ici)*
1.  **Sources** : Logs Web, Transactions.
2.  **Transport** : Apache Kafka.
3.  **Traitement** : Spark (Streaming) & Hive (Batch).
4.  **Stockage** : HDFS (Parquet), HBase (NoSQL).
5.  **Viz** : Requêtes SQL Impala / Dashboard.

---

## Slide 4 : Ingestion des Données (Kafka)
*   **Producer Python** : Simule 3 types d'événements (Clicks, Achats, Inventaire).
*   **Topics** : Partitionnés pour la parallélisation.
*   Volume simulé : 100 événements/seconde.

---

## Slide 5 : Traitement Streaming (Spark/Scala)
*   Lecture structurée (Structured Streaming).
*   Parsing JSON -> DataFrame typé.
*   **Double écriture** :
    *   HDFS (Archivage long terme, format Parquet).
    *   HBase (Compteurs temps réel, ex: Chiffre d'affaire des 5 dernières minutes).

---

## Slide 6 : Analyse Batch (Hive & Airflow)
*   **Airflow DAG** : Exécution quotidienne à minuit.
*   **Hive** : Calcul des KPIs agrégés (Revenu par catégorie, Top produits).
*   **Optimisation** : Tables partitionnées par Date/Heure.

---

## Slide 7 : Démonstration
*   Lancement des conteneurs Docker.
*   Visualisation du flux de données dans Spark UI.
*   Requête SQL en direct sur les données ingérées.
*   Vérification du DAG Airflow.

---

## Slide 8 : Conclusion
*   Compétences acquises : Intégration de systèmes distribués.
*   Défis : Configuration réseau Docker, gestion des schémas.
*   Perspectives : Ajouter un dashboard Grafana, Machine Learning sur les données clients.
