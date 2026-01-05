#!/bin/bash

# ============================================================
# Start Producer - E-commerce Transaction Generator (WSL)
# ============================================================

echo "============================================================"
echo "🛒 STARTING E-COMMERCE PRODUCER (WSL)"
echo "============================================================"
echo ""
echo "📡 Generating transactions to Kafka topic: ecommerce-transactions"
echo "🛑 Press Ctrl+C to stop"
echo ""

docker exec -it spark-master python3 /opt/spark-apps/producer.py
