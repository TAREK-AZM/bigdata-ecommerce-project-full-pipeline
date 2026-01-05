from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import glob

app = Flask(__name__, static_folder='../dashboard')
CORS(app)

DATA_PATH = "/tmp/ecommerce-data/raw"

@app.route('/')
def index():
    return send_from_directory('../dashboard', 'dashboard.html')

@app.route('/api/stats')
def get_stats():
    try:
        # Check if data exists
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "No data available yet"}), 404
        
        # Read all parquet files
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
        
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        total_transactions = len(df)
        total_users = df['user_id'].nunique()
        total_cities = df['city'].nunique()
        total_categories = df['category'].nunique()
        
        revenue_total = float(df['amount'].sum())
        montant_moy = float(df['amount'].mean())
        quantite_total = int(df['quantity'].sum())
        
        return jsonify({
            "total_transactions": total_transactions,
            "total_users": total_users,
            "total_cities": total_cities,
            "total_categories": total_categories,
            "revenue_total": round(revenue_total, 2),
            "montant_moy": round(montant_moy, 2),
            "quantite_total": quantite_total
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories')
def get_categories():
    try:
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
            
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        category_data = df.groupby('category').agg({
            'amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        category_data.columns = ['category', 'revenue', 'transactions']
        category_data = category_data.sort_values('revenue', ascending=False)
        
        return jsonify({
            "labels": category_data['category'].tolist(),
            "revenue": [round(float(x), 2) for x in category_data['revenue']],
            "transactions": [int(x) for x in category_data['transactions']]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cities')
def get_cities():
    try:
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
            
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        city_data = df.groupby('city')['amount'].sum().reset_index()
        city_data.columns = ['city', 'revenue']
        city_data = city_data.sort_values('revenue', ascending=False)
        
        return jsonify({
            "labels": city_data['city'].tolist(),
            "revenue": [round(float(x), 2) for x in city_data['revenue']]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payments')
def get_payments():
    try:
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
            
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        payment_data = df.groupby('payment_method').agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        payment_data.columns = ['payment_method', 'transactions', 'revenue']
        payment_data = payment_data.sort_values('transactions', ascending=False)
        
        return jsonify({
            "labels": payment_data['payment_method'].tolist(),
            "transactions": [int(x) for x in payment_data['transactions']],
            "revenue": [round(float(x), 2) for x in payment_data['revenue']]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/top-transactions')
def get_top_transactions():
    try:
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
            
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        top_transactions = df.nlargest(10, 'amount')
        
        return jsonify([{
            "transaction_id": str(row['transaction_id'])[:8] + "...",
            "user_id": row['user_id'],
            "city": row['city'],
            "category": row['category'],
            "amount": round(float(row['amount']), 2),
            "quantity": int(row['quantity']),
            "payment_method": row['payment_method'],
            "timestamp": str(row['timestamp'])
        } for _, row in top_transactions.iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recent-transactions')
def get_recent_transactions():
    try:
        parquet_files = glob.glob(f"{DATA_PATH}/*.parquet")
        if not parquet_files:
            return jsonify({"error": "No data files found"}), 404
            
        df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
        
        # Sort by timestamp and get last 20
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        recent = df.nlargest(20, 'timestamp')
        
        return jsonify([{
            "user_id": row['user_id'],
            "city": row['city'],
            "category": row['category'],
            "amount": round(float(row['amount']), 2),
            "payment_method": row['payment_method'],
            "timestamp": str(row['timestamp'])
        } for _, row in recent.iterrows()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 DASHBOARD SERVER STARTING")
    print("=" * 70)
    print("📊 Dashboard: http://localhost:5000")
    print("🔄 Auto-refresh: Every 10 seconds")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5000, debug=True)
