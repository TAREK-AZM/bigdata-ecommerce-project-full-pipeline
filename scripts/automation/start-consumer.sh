#!/bin/bash

# ============================================================
# Start Consumer - Spark Streaming Consumer (WSL)
# ============================================================

echo "============================================================"
echo "⚡ STARTING SPARK STREAMING CONSUMER (WSL)"
echo "============================================================"
echo ""
echo "📊 Processing transactions from Kafka..."
echo "💾 Saving to: /tmp/ecommerce-data/raw/*.parquet"
echo "🛑 Press Ctrl+C to stop"
echo ""

docker exec -it spark-master /opt/spark/bin/spark-submit \
    --master local[2] \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    /opt/spark-apps/consumer_spark.py
