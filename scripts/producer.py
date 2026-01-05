from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime
import uuid

# Configuration
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

categories = ['Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Books', 'Toys']
payment_methods = ['Credit Card', 'PayPal', 'Wire Transfer', 'Cryptocurrency']
cities = ['Casablanca', 'Rabat', 'Marrakech', 'Fes', 'Tanger', 'Agadir']

print("=" * 60)
print("🛒  PRODUCTEUR E-COMMERCE - DÉMARRAGE")
print("=" * 60)
print(f"📦 Catégories : {', '.join(categories)}")
print(f"📡 Topic Kafka : ecommerce-transactions")
print("=" * 60)

try:
    count = 0
    while True:
        data = {
            'transaction_id': str(uuid.uuid4()),
            'user_id': f'USER_{random.randint(100, 999)}',
            'city': random.choice(cities),
            'category': random.choice(categories),
            'amount': round(random.uniform(10.0, 500.0), 2),
            'quantity': random.randint(1, 5),
            'payment_method': random.choice(payment_methods),
            'timestamp': datetime.now().isoformat()
        }
        
        producer.send('ecommerce-transactions', value=data)
        count += 1
        
        if count % 10 == 0:
            print(f"✅ {count} transactions envoyées - Dernière: {data['category']} {data['amount']}€")
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print(f"\n⏹️  Arrêt - Total: {count} transactions")
    producer.close()
