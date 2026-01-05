# 🛒 Projet Big Data - Analyse des Transactions E-commerce en Temps Réel

> **Étudiant :** AL AZAMI TAREK  
> **Établissement :** ENSA  
> **Année Universitaire :** 2025-2026  
> **Encadrant :** Professeur Hassan BADIR

---

## 📋 Table des Matières

- [Vue d'Ensemble](#vue-densemble)
- [Architecture Technique](#architecture-technique)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation et Configuration](#installation-et-configuration)
- [Exécution du Projet](#exécution-du-projet)
- [Résultats](#résultats)
- [Structure du Projet](#structure-du-projet)

---

## 🎯 Vue d'Ensemble

Ce projet implémente un **pipeline Big Data complet** pour l'analyse en temps réel des transactions e-commerce, utilisant les technologies Apache Kafka, Spark Streaming et HDFS dans un environnement containerisé Docker.

### Objectifs

✅ Ingestion de transactions e-commerce en temps réel avec **Apache Kafka**  
✅ Traitement streaming avec **Apache Spark Streaming**  
✅ Stockage distribué avec **HDFS** (format Parquet)  
✅ Agrégations du chiffre d'affaires par catégorie de produits  
✅ Analyse statistique et génération de rapports  

### Cas d'Usage

**Analyse de ventes** : Simulation de transactions provenant de différentes villes marocaines couvrant plusieurs catégories (Électronique, Mode, Maison, etc.) pour suivre le chiffre d'affaires en temps réel.

---

## 🏗️ Architecture Technique
```
┌─────────────────────────────────────────────────────────────┐
│                PIPELINE BIG DATA E-COMMERCE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📡 Producteur Python (Transactions simulées)               │
│      ↓                                                      │
│  🔄 Apache Kafka (Topic: ecommerce-transactions)            │
│      ↓                                                      │
│  ⚡ Apache Spark Streaming (Mode Local)                     │
│      ├─ Console (Affichage temps réel)                     │
│      └─ HDFS (Stockage Parquet)                            │
│      ↓                                                      │
│  💾 HDFS (/tmp/ecommerce-data/raw/*.parquet)                │
│      ↓                                                      │
│  📊 Analyse Spark SQL (Chiffre d'Affaires & Tendances)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Composants du Cluster Docker

| Conteneur | Rôle | Ports |
|-----------|------|-------|
| **zookeeper** | Coordination Kafka | 2181 |
| **kafka** | Message Broker | 9092 |
| **spark-master** | Nœud Maître Spark | 8080, 7077, 4040 |
| **spark-worker** | Nœud Worker Spark | - |
| **namenode** | HDFS NameNode | 9870, 9000 |
| **datanode** | HDFS DataNode | - |

---

## 🛠️ Technologies Utilisées

### Big Data Stack

- **Apache Kafka 7.5.0** - Ingestion streaming
- **Apache Spark 3.5.0** - Traitement distribué
- **Apache Hadoop 3.2.1** - Stockage HDFS
- **Apache Zookeeper 7.5.0** - Coordination

### Développement

- **Python 3.x** - Scripts producteur/analyse
- **Docker & Docker Compose** - Containerisation
- **kafka-python** - Client Kafka Python

### Formats de Données

- **JSON** - Format des messages Kafka
- **Parquet + Snappy** - Stockage compressé HDFS

---

## 📦 Installation et Configuration

### Prérequis

- Docker Desktop installé et démarré
- Python 3.x avec pip
- 8 GB RAM minimum
- 20 GB espace disque

### Étape 1 : Cloner le Projet
```bash
git clone https://github.com/TAREK-AZM/bigdata-ecommerce-project-full-pipeline.git
cd bigdata-ecommerce-project-full-pipeline
```

### Étape 2 : Démarrer l'Infrastructure Docker
```powershell
# Démarrer tous les conteneurs
docker-compose up -d

# Vérifier le statut
docker-compose ps
```

**Résultat attendu :** Tous les conteneurs doivent être **Up**

### Étape 3 : Installer les Dépendances
```powershell
# Installer kafka-python dans Spark
docker exec -it -u root spark-master pip install kafka-python

# Fixer les permissions Ivy (pour Spark)
docker exec -it -u root spark-master bash -c "mkdir -p /home/spark/.ivy2/cache /home/spark/.ivy2/jars && chown -R spark:spark /home/spark/.ivy2 && chmod -R 777 /home/spark/.ivy2"
```

### Étape 4 : Créer le Topic Kafka
```powershell
docker exec -it kafka kafka-topics --create --topic ecommerce-transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

---

## 🚀 Quick Start (Automated)

The easiest way to run the project (especially on WSL/Linux) is using the provided bash scripts.

### 1. Setup Environment
Run this once to start containers and install dependencies:
```bash
./scripts/automation/setup.sh
```

### 2. Start Everything
This starts the dashboard, consumer, and producer automatically:
```bash
./scripts/automation/start-all.sh
```
*   The **Dashboard** will be available at [http://localhost:5000](http://localhost:5000)
*   The **Consumer** will start processing transactions
*   The **Producer** will start generating fake data

### 3. Run Analysis Report
To generate a statistical report from the collected data:
```bash
./scripts/automation/run-analysis.sh
```

### 4. Stop Everything
To stop all containers gracefully:
```bash
./scripts/automation/stop-all.sh
```

#### 4. Run Batch Analysis (Optional)
```powershell
.\scripts\automation\run-analysis.ps1
```
Generates a detailed report: `rapport_ecommerce.md`

#### 5. Stop Everything
```powershell
.\scripts\automation\stop-all.ps1
```

### Individual Component Scripts

If you prefer to run components separately:

```powershell
# Start producer only
.\scripts\automation\start-producer.ps1

# Start consumer only
.\scripts\automation\start-consumer.ps1

# Run analysis
.\scripts\automation\run-analysis.ps1
```

---

## 🔧 Manual Execution (Advanced)

If you prefer manual control over each step:

## 🚀 Exécution du Projet

### Terminal 1 : Lancer le Producteur E-commerce
```powershell
docker exec -it spark-master python3 /opt/spark-apps/producer.py
```

**Sortie attendue :**
```
============================================================
🛒  PRODUCTEUR E-COMMERCE - DÉMARRAGE
============================================================
📦 Catégories : Electronics, Fashion, Home & Garden, Sports...
📡 Topic Kafka : ecommerce-transactions
============================================================
✅ 10 transactions envoyées - Dernière: Electronics 245.50€
✅ 20 transactions envoyées - Dernière: Fashion 89.99€
```

### Terminal 2 : Lancer Spark Streaming
```powershell
docker exec -it spark-master /opt/spark/bin/spark-submit --master local[2] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /opt/spark-apps/consumer_spark.py
```

**Sortie attendue :**
```
======================================================================
🚀 SPARK STREAMING - ANALYSE E-COMMERCE
======================================================================
✅ Pipeline actif !
📊 Console : Transactions brutes (10s)
📈 Console : Chiffre d'affaires par catégorie (30s)
💾 HDFS : /tmp/ecommerce-data/raw
```

### Laisser Tourner 2-3 Minutes

Les deux terminaux doivent rester actifs pour collecter des données.

### Arrêter les Processus

Appuyez sur **Ctrl+C** dans chaque terminal (producteur et consumer).

### Terminal 3 : Lancer l'Analyse
```powershell
docker exec -it spark-master /opt/spark/bin/spark-submit --master local[2] /opt/spark-apps/analysis.py
```

### Récupérer le Rapport
```powershell
docker cp spark-master:/tmp/rapport.md ./rapport_final.md
```

---

## 📊 Résultats

### Métriques de Performance

| Métrique | Valeur |
|----------|--------|
| **Transactions traitées** | 2000+ |
| **Villes couvertes** | 6 |
| **Catégories produits** | 5 |
| **Latence moyenne** | < 5 secondes |
| **Volume de données** | ~50 MB/jour |
| **Format de stockage** | Parquet (Snappy) |

### Exemple de Données Collectées
```
+----------+----------+-----------+--------+--------------------------+
|transaction_id|product_category|amount |payment_method|city      |timestamp          |
+--------------+----------------+-------+--------------+----------+-------------------+
|TXN_10023     |Electronics     |245.50 |Credit Card   |Casablanca|2025-12-28 20:15:12|
|TXN_10024     |Fashion         |89.99  |Cash          |Marrakech |2025-12-28 20:15:13|
|TXN_10025     |Home & Garden   |120.00 |Mobile App    |Rabat     |2025-12-28 20:15:14|
+--------------+----------------+-------+--------------+----------+-------------------+
```

### Agrégations par Ville
```
+----------+------------------+--------+--------+------------+
|city      |total_revenue     |transaction_count|avg_basket|top_category|
+----------+------------------+-----------------+----------+------------+
|Marrakech |15420.50          |145              |106.34    |Fashion     |
|Casablanca|23500.00          |210              |111.90    |Electronics |
|Agadir    |9800.75           |98               |100.01    |Sports      |
+----------+------------------+-----------------+----------+------------+
```

### Alertes Détectées

- 💰 **Transactions > 1000 MAD :** 15 occurrences (Ventes High-Ticket)
- 📈 **Pic de ventes :** 20:00 - 21:00 (Heure de pointe)

---

## 📁 Structure du Projet
```
bigdata-ecommerce-project-full-pipeline/
├── AL AZAMI TAREK RAPPORT BIG DATA PANACHE PROJECT.pdf
├── README.md                   # Ce fichier
├── dashboard/
│   └── dashboard.html          # Dashboard de visualisation
├── data/                       # Données
├── docker-compose.yml          # Configuration Docker
├── hadoop.env                  # Variables d'environnement Hadoop
├── rapport_ecommerce.md        # Rapport d'analyse généré
├── rapport_projet.tex          # Rapport LaTeX source
├── requirements.txt            # Dépendances Python
├── screenShots/
│   ├── 1.png
│   └── 2.png
└── scripts/
    ├── analysis.py             # Analyse finale
    ├── automation/             # Scripts d'automatisation
    │   ├── README.md
    │   ├── run-analysis.sh
    │   ├── setup.sh
    │   ├── start-all.sh
    │   ├── start-consumer.sh
    │   ├── start-producer.sh
    │   └── stop-all.sh
    ├── consumer_spark.py       # Consumer Spark Streaming
    ├── dashboard_server.py     # Serveur Dashboard
    └── producer.py             # Producteur Kafka
```

### Description des Scripts

#### 1. `producer.py`

Simule des transactions e-commerce en temps réel avec des données réalistes.

**Fonctionnalités :**
- Génération aléatoire de montants et catégories
- Simulation de méthodes de paiement (Carte, Cash, Mobile)
- Envoi à Kafka toutes les 1 seconde
- 6 villes marocaines (Casablanca, Rabat, Marrakech, etc.)

#### 2. `consumer_spark.py`

Consumer Spark Streaming qui traite les données en temps réel.

**Fonctionnalités :**
- Lecture depuis Kafka
- Agrégations par fenêtres de 30 secondes
- Affichage console (données brutes + agrégations)
- Sauvegarde HDFS en format Parquet

#### 3. `analysis.py`

Script d'analyse batch des données stockées.

**Fonctionnalités :**
- Lecture des fichiers Parquet
- Calcul de statistiques par ville (Chiffre d'affaires total, Panier moyen)
- Identification des catégories les plus vendues
- Génération de rapport Markdown structuré

---

## 🌐 Interfaces Web

- **Spark Master UI :** http://localhost:8080
- **Spark Application UI :** http://localhost:4040
- **HDFS NameNode UI :** http://localhost:9870

---

## 🔧 Dépannage

### Problème : Conteneurs ne démarrent pas
```powershell
docker-compose down
docker system prune -f
docker-compose up -d
```

### Problème : Permissions Ivy Cache
```powershell
docker exec -it -u root spark-master bash -c "mkdir -p /home/spark/.ivy2/cache && chown -R spark:spark /home/spark/.ivy2 && chmod -R 777 /home/spark/.ivy2"
```

### Problème : Topic Kafka existe déjà
```powershell
docker exec -it kafka kafka-topics --delete --topic ecommerce-transactions --bootstrap-server localhost:9092
```

---

## 📚 Références

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Streaming Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- [Hadoop HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)

---

## 👨‍💻 Auteur

**AL AZAMI TAREK**  
Étudiant en Big Data  
ENSA - 2025/2026

---

## 📄 Licence

Ce projet est réalisé dans le cadre d'un travail pratique universitaire.

---

**Dernière mise à jour :** Décembre 2025