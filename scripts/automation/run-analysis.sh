#!/bin/bash

# ============================================================
# Run Analysis - Batch Analysis of E-commerce Data (WSL)
# ============================================================

echo "============================================================"
echo "📊 RUNNING E-COMMERCE ANALYSIS (WSL)"
echo "============================================================"
echo ""
echo "📈 Analyzing parquet files..."
echo ""

docker exec -it spark-master /opt/spark/bin/spark-submit \
    --master local[2] \
    /opt/spark-apps/analysis.py

echo ""
echo "============================================================"
echo "📋 Retrieving Report..."
echo "============================================================"

docker cp spark-master:/tmp/rapport_ecommerce.md ./rapport_ecommerce.md

if [ $? -eq 0 ]; then
    echo "✅ Report saved to: rapport_ecommerce.md"
else
    echo "⚠️  Could not retrieve report"
fi
