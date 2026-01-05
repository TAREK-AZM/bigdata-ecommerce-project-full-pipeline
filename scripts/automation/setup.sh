#!/bin/bash

# ============================================================
# Setup Script - E-commerce Analytics Platform (WSL)
# ============================================================

echo "============================================================"
echo "🚀 SETUP - E-COMMERCE ANALYTICS PLATFORM (WSL)"
echo "============================================================"
echo ""

# Step 1: Start Docker Containers
echo "📦 Step 1/4: Starting Docker containers..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start Docker containers"
    exit 1
fi

echo "✅ Docker containers started"
echo ""

# Wait for services to initialize
echo "⏳ Waiting 30 seconds for services to initialize..."
sleep 30

# Step 2: Install Dependencies
echo "📦 Step 2/4: Installing dependencies in Spark..."
docker exec -u root spark-master pip install -q kafka-python

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Step 3: Fix Ivy Permissions
echo "🔧 Step 3/4: Fixing Spark Ivy permissions..."
docker exec -u root spark-master bash -c "mkdir -p /home/spark/.ivy2/cache /home/spark/.ivy2/jars && chown -R spark:spark /home/spark/.ivy2 && chmod -R 777 /home/spark/.ivy2"

if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Could not fix Ivy permissions"
fi

echo "✅ Permissions configured"
echo ""

# Step 4: Create Kafka Topic
echo "📡 Step 4/4: Creating Kafka topic..."

# Check if topic already exists
if docker exec kafka kafka-topics --list --bootstrap-server localhost:9092 2>/dev/null | grep -q "ecommerce-transactions"; then
    echo "ℹ️  Topic 'ecommerce-transactions' already exists"
else
    docker exec kafka kafka-topics --create --topic ecommerce-transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create Kafka topic"
        exit 1
    fi
    
    echo "✅ Kafka topic created"
fi

echo ""
echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "📊 Web Interfaces Available:"
echo "   - Spark Master:  http://localhost:8080"
echo "   - Spark App:     http://localhost:4040"
echo "   - HDFS:          http://localhost:9870"
echo "   - Dashboard:     http://localhost:5000"
echo ""
echo "🎯 Next Steps:"
echo "   1. Run: ./scripts/automation/start-all.sh"
echo "   2. Or run components individually:"
echo "      - ./scripts/automation/start-producer.sh"
echo "      - ./scripts/automation/start-consumer.sh"
echo ""
