#!/bin/bash

# ============================================================
# Stop All - Stop E-commerce Analytics Pipeline (WSL)
# ============================================================

echo "============================================================"
echo "🛑 STOPPING E-COMMERCE ANALYTICS PIPELINE (WSL)"
echo "============================================================"
echo ""

echo "🔄 Stopping Docker containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "✅ All containers stopped"
else
    echo "⚠️  Some containers may still be running"
fi

echo ""
echo "============================================================"
echo "✅ SHUTDOWN COMPLETE"
echo "============================================================"
echo ""
echo "💡 To start again, run: ./scripts/automation/start-all.sh"
echo ""
