#!/bin/bash

# ============================================================
# Start All - Complete E-commerce Analytics Pipeline (WSL)
# ============================================================

echo "============================================================"
echo "🚀 STARTING COMPLETE E-COMMERCE ANALYTICS PIPELINE (WSL)"
echo "============================================================"
echo ""

# Check if setup has been run
echo "🔍 Checking if setup is complete..."
containers=$(docker ps --format "{{.Names}}" 2>/dev/null)

if ! echo "$containers" | grep -q "kafka" || ! echo "$containers" | grep -q "spark-master" || ! echo "$containers" | grep -q "dashboard"; then
    echo "⚠️  Infrastructure not ready. Running setup first..."
    echo ""
    ./scripts/automation/setup.sh
    echo ""
fi

echo "============================================================"
echo "🎯 STARTING SERVICES"
echo "============================================================"
echo ""

# Create data directory with proper permissions
echo "📁 Creating data directory with proper permissions..."
docker exec -u root spark-master mkdir -p /tmp/ecommerce-data/raw
docker exec -u root spark-master chmod -R 777 /tmp/ecommerce-data
echo "✅ Data directory ready"
echo ""

# Start dashboard in background
echo "📊 Starting Dashboard..."
gnome-terminal -- bash -c "docker-compose up dashboard; exec bash" 2>/dev/null || \
xterm -e "docker-compose up dashboard" 2>/dev/null || \
docker-compose up dashboard &
sleep 5
echo "✅ Dashboard started at http://localhost:5000"
echo ""

# Start consumer in new terminal
echo "⚡ Starting Spark Consumer..."
gnome-terminal -- bash -c "./scripts/automation/start-consumer.sh; exec bash" 2>/dev/null || \
xterm -e "./scripts/automation/start-consumer.sh" 2>/dev/null || \
echo "⚠️  Could not open new terminal. Run manually: ./scripts/automation/start-consumer.sh"
sleep 10
echo "✅ Consumer started"
echo ""

# Start producer in new terminal
echo "🛒 Starting Producer..."
gnome-terminal -- bash -c "./scripts/automation/start-producer.sh; exec bash" 2>/dev/null || \
xterm -e "./scripts/automation/start-producer.sh" 2>/dev/null || \
echo "⚠️  Could not open new terminal. Run manually: ./scripts/automation/start-producer.sh"
sleep 3
echo "✅ Producer started"
echo ""

echo "============================================================"
echo "✅ ALL SERVICES RUNNING!"
echo "============================================================"
echo ""
echo "📊 Access Points:"
echo "   - Dashboard:     http://localhost:5000  (Real-time Analytics)"
echo "   - Spark Master:  http://localhost:8080  (Cluster Status)"
echo "   - Spark App:     http://localhost:4040  (Job Details)"
echo "   - HDFS:          http://localhost:9870  (Storage)"
echo ""
echo "🎯 What's Happening:"
echo "   1. Producer is generating e-commerce transactions"
echo "   2. Spark is processing them in real-time"
echo "   3. Data is being saved to parquet files"
echo "   4. Dashboard is showing live analytics"
echo ""
echo "⏱️  Let it run for 2-3 minutes to collect data"
echo ""
echo "🛑 To Stop:"
echo "   - Close the Producer and Consumer terminals (Ctrl+C)"
echo "   - Run: docker-compose down"
echo ""
echo "📈 To Run Analysis:"
echo "   - Run: ./scripts/automation/run-analysis.sh"
echo ""
