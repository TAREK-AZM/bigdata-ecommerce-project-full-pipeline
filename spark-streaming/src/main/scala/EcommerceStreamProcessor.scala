package com.ecommerce.bigdata

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._

object EcommerceStreamProcessor {
  def main(args: Array[String]): Unit = {
    // Initialisation de Spark Session
    val spark = SparkSession.builder()
      .appName("EcommerceStreamProcessor")
      .config("spark.master", "local[*]") // Pour dev, utiliser cluster en prod
      .config("spark.hadoop.dfs.client.use.datanode.hostname", "true")
      .getOrCreate()

    import spark.implicits._
    spark.sparkContext.setLogLevel("WARN")

    // Configuration Kafka
    val kafkaBootstrapServers = "kafka:29092"

    // Schémas des données
    val clickSchema = new StructType()
      .add("event_id", StringType)
      .add("user_id", StringType)
      .add("product_id", StringType)
      .add("category", StringType)
      .add("page_url", StringType)
      .add("timestamp", LongType)
      .add("session_id", StringType)
      .add("device", StringType)
      .add("event_date", StringType)
      .add("event_hour", IntegerType)

    val purchaseSchema = new StructType()
      .add("transaction_id", StringType)
      .add("user_id", StringType)
      .add("product_id", StringType)
      .add("category", StringType)
      .add("quantity", IntegerType)
      .add("unit_price", DoubleType)
      .add("total_amount", DoubleType)
      .add("payment_method", StringType)
      .add("timestamp", LongType)
      .add("status", StringType)
      .add("event_date", StringType)
      .add("event_hour", IntegerType)

    // Lecture du flux Kafka pour les CLICS
    val clicksStream = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", kafkaBootstrapServers)
      .option("subscribe", "ecommerce-clicks")
      .option("startingOffsets", "latest")
      .load()

    val parsedClicks = clicksStream
      .selectExpr("CAST(value AS STRING)")
      .select(from_json($"value", clickSchema).as("data"))
      .select("data.*")

    // Traitement et écriture par lots sur HDFS (partitionné par date/heure)
    val clicksQuery = parsedClicks.writeStream
      .format("parquet")
      .option("path", "hdfs://namenode:9000/data/ecommerce/clicks")
      .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/clicks")
      .partitionBy("event_date", "event_hour")
      .trigger(Trigger.ProcessingTime("1 minute"))
      .start()

    // Lecture du flux Kafka pour les ACHATS
    val purchasesStream = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", kafkaBootstrapServers)
      .option("subscribe", "ecommerce-purchases")
      .option("startingOffsets", "latest")
      .load()

    val parsedPurchases = purchasesStream
      .selectExpr("CAST(value AS STRING)")
      .select(from_json($"value", purchaseSchema).as("data"))
      .select("data.*")

    // Enrichissement simple : Calcul du revenu en temps réel (fenêtre glissante de 10 min)
    val revenueByWindow = parsedPurchases
      .groupBy(
        window($"timestamp".cast("timestamp"), "10 minutes", "5 minutes"),
        $"category"
      )
      .agg(sum("total_amount").as("revenue"))

    // Écriture Console pour debug (ou HBase en production)
    val revenueQuery = revenueByWindow.writeStream
      .outputMode("update")
      .format("console")
      .option("truncate", "false")
      .trigger(Trigger.ProcessingTime("1 minute"))
      .start()
      
    // Écriture des données brutes achats sur HDFS
    val purchasesQuery = parsedPurchases.writeStream
      .format("parquet")
      .option("path", "hdfs://namenode:9000/data/ecommerce/purchases")
      .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/purchases")
      .partitionBy("event_date", "event_hour")
      .trigger(Trigger.ProcessingTime("1 minute"))
      .start()

    // Attente de la terminaison
    spark.streams.awaitAnyTermination()
  }
}
