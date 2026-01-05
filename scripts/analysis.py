from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, asc, avg, max, min, count, sum as spark_sum, round as spark_round
from datetime import datetime

spark = SparkSession.builder \
    .appName("E-commerce Analysis") \
    .master("local[2]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("=" * 70)
print("� ANALYSE DES TRANSACTIONS E-COMMERCE")
print("=" * 70)

try:
    # Lire les données
    df = spark.read.parquet("/tmp/ecommerce-data/raw/*.parquet")
    
    total_transactions = df.count()
    total_users = df.select('user_id').distinct().count()
    total_cities = df.select('city').distinct().count()
    total_categories = df.select('category').distinct().count()
    
    print(f"\n✅ {total_transactions:,} transactions analysées")
    print(f"� {total_users} utilisateurs uniques")
    print(f"� {total_cities} villes")
    print(f"🏷️  {total_categories} catégories\n")
    
    # Statistiques globales
    print("=" * 70)
    print("💰 STATISTIQUES GLOBALES")
    print("=" * 70)
    
    stats = df.select(
        spark_sum("amount").alias("revenue_total"),
        avg("amount").alias("montant_moy"),
        max("amount").alias("montant_max"),
        min("amount").alias("montant_min"),
        avg("quantity").alias("quantite_moy"),
        spark_sum("quantity").alias("quantite_total")
    ).collect()[0]
    
    print(f"Chiffre d'affaires total : {stats['revenue_total']:,.2f}€")
    print(f"Montant moyen            : {stats['montant_moy']:.2f}€")
    print(f"Montant maximum          : {stats['montant_max']:.2f}€")
    print(f"Montant minimum          : {stats['montant_min']:.2f}€")
    print(f"Quantité moyenne         : {stats['quantite_moy']:.2f} articles")
    print(f"Quantité totale          : {stats['quantite_total']:,} articles")
    
    # Analyse par catégorie
    print("\n" + "=" * 70)
    print("🏷️  ANALYSE PAR CATÉGORIE")
    print("=" * 70)
    
    df.groupBy("category") \
        .agg(
            spark_sum("amount").alias("revenue"),
            count("*").alias("transactions"),
            avg("amount").alias("montant_moy"),
            spark_sum("quantity").alias("articles_vendus")
        ) \
        .withColumn("revenue", spark_round(col("revenue"), 2)) \
        .withColumn("montant_moy", spark_round(col("montant_moy"), 2)) \
        .orderBy(desc("revenue")) \
        .show(truncate=False)
    
    # Analyse par ville
    print("=" * 70)
    print("📍 ANALYSE PAR VILLE")
    print("=" * 70)
    
    df.groupBy("city") \
        .agg(
            spark_sum("amount").alias("revenue"),
            count("*").alias("transactions"),
            avg("amount").alias("montant_moy")
        ) \
        .withColumn("revenue", spark_round(col("revenue"), 2)) \
        .withColumn("montant_moy", spark_round(col("montant_moy"), 2)) \
        .orderBy(desc("revenue")) \
        .show(truncate=False)
    
    # Analyse par méthode de paiement
    print("=" * 70)
    print("💳 ANALYSE PAR MÉTHODE DE PAIEMENT")
    print("=" * 70)
    
    payment_stats = df.groupBy("payment_method") \
        .agg(
            count("*").alias("transactions"),
            spark_sum("amount").alias("revenue")
        ) \
        .withColumn("revenue", spark_round(col("revenue"), 2)) \
        .orderBy(desc("transactions"))
    
    payment_stats.show(truncate=False)
    
    # Top utilisateurs
    print("=" * 70)
    print("👥 TOP 10 UTILISATEURS")
    print("=" * 70)
    
    df.groupBy("user_id") \
        .agg(
            count("*").alias("transactions"),
            spark_sum("amount").alias("total_depense")
        ) \
        .withColumn("total_depense", spark_round(col("total_depense"), 2)) \
        .orderBy(desc("total_depense")) \
        .show(10, truncate=False)
    
    # Transactions importantes
    print("=" * 70)
    print("💎 TOP 10 TRANSACTIONS")
    print("=" * 70)
    
    df.select("transaction_id", "user_id", "city", "category", "amount", "quantity", "payment_method") \
        .orderBy(desc("amount")) \
        .show(10, truncate=False)
    
    # Générer rapport
    category_top = df.groupBy("category") \
        .agg(spark_sum("amount").alias("revenue")) \
        .orderBy(desc("revenue")) \
        .first()
    
    city_top = df.groupBy("city") \
        .agg(spark_sum("amount").alias("revenue")) \
        .orderBy(desc("revenue")) \
        .first()
    
    rapport = f"""# RAPPORT E-COMMERCE - {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Résumé
- **Transactions** : {total_transactions:,}
- **Utilisateurs** : {total_users}
- **Villes** : {total_cities}
- **Catégories** : {total_categories}

## Statistiques Financières
- Chiffre d'affaires : {stats['revenue_total']:,.2f}€
- Montant moyen : {stats['montant_moy']:.2f}€
- Montant max : {stats['montant_max']:.2f}€
- Montant min : {stats['montant_min']:.2f}€

## Performance
- Catégorie #1 : {category_top['category']} ({category_top['revenue']:,.2f}€)
- Ville #1 : {city_top['city']} ({city_top['revenue']:,.2f}€)
- Articles vendus : {stats['quantite_total']:,}

**Projet Big Data E-commerce - ENSA 2024/2025**
"""
    
    with open("/tmp/rapport_ecommerce.md", "w") as f:
        f.write(rapport)
    
    print("\n" + "=" * 70)
    print("✅ Rapport sauvegardé : /tmp/rapport_ecommerce.md")
    print("📋 Copier : docker cp spark-master:/tmp/rapport_ecommerce.md ./")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    import traceback
    traceback.print_exc()

spark.stop()