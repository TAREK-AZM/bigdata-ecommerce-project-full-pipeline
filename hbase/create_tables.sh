#!/bin/bash
# Script de création des tables HBase

echo "create 'product_metrics', 'stats', 'inventory'" | hbase shell
echo "create 'user_profiles', 'behavior', 'preferences'" | hbase shell
echo "create 'real_time_revenue', 'metrics'" | hbase shell

echo "Tables HBase créées avec succès."
