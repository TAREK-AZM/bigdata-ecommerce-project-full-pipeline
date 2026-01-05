from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, avg, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# Session Spark en mode local
spark = SparkSession.builder \
    .appName("E-commerce Transaction Analysis") \
    .master("local[2]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("🚀 SPARK STREAMING - ANALYSE E-COMMERCE")
print("=" * 70)

# Schéma des données
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("city", StringType(), True),
    StructField("category", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("payment_method", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# Lire depuis Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "ecommerce-transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Parser JSON
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
parsed_df = parsed_df.withColumn("timestamp", col("timestamp").cast(TimestampType()))
parsed_df_with_watermark = parsed_df.withWatermark("timestamp", "1 minute")

# Agrégations : Chiffre d'affaires par catégorie
aggregated_df = parsed_df_with_watermark \
    .groupBy(window(col("timestamp"), "1 minute"), "category") \
    .agg(
        sum("amount").alias("total_revenue"),
        avg("amount").alias("avg_transaction"),
        count("transaction_id").alias("num_transactions")
    )

# Affichage console - Transactions brutes
query_console = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='10 seconds') \
    .start()

# Affichage console - Agrégations
query_aggregated = aggregated_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='30 seconds') \
    .start()

# Sauvegarde HDFS
query_hdfs = parsed_df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/tmp/ecommerce-data/raw") \
    .option("checkpointLocation", "/tmp/ecommerce-data/checkpoints") \
    .trigger(processingTime='30 seconds') \
    .start()

print("✅ Pipeline actif !")
print("📊 Console : Transactions brutes (10s)")
print("📈 Console : Chiffre d'affaires par catégorie (30s)")
print("💾 HDFS : /tmp/ecommerce-data/raw")
print("🛑 Ctrl+C pour arrêter")
print("=" * 70)

query_console.awaitTermination()
