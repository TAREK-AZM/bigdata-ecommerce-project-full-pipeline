import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPICS = {
    'clicks': 'ecommerce-clicks',
    'purchases': 'ecommerce-purchases',
    'inventory': 'ecommerce-inventory'
}

# Données de simulation
USERS = [f"user_{i:04d}" for i in range(1, 501)]
PRODUCTS = [f"prod_{i:03d}" for i in range(1, 101)]
CATEGORIES = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
PAGES = ['/home', '/product', '/cart', '/checkout', '/profile']

class EcommerceDataGenerator:
    def __init__(self):
        self.producer = None
        self.connect_kafka()
    
    def connect_kafka(self):
        """Connexion à Kafka avec retry"""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=[KAFKA_BROKER],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    api_version=(0, 10, 1)
                )
                print("✓ Connecté à Kafka")
                return
            except NoBrokersAvailable:
                print(f"Tentative {attempt + 1}/{max_retries} - Kafka non disponible")
                time.sleep(5)
        raise Exception("Impossible de se connecter à Kafka")
    
    def generate_click_event(self):
        """Génère un événement de clic"""
        return {
            'event_id': f"click_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            'user_id': random.choice(USERS),
            'product_id': random.choice(PRODUCTS),
            'category': random.choice(CATEGORIES),
            'page_url': random.choice(PAGES),
            'timestamp': int(time.time() * 1000),
            'session_id': f"session_{random.randint(10000, 99999)}",
            'device': random.choice(['mobile', 'desktop', 'tablet']),
            'event_date': datetime.now().strftime('%Y-%m-%d'),
            'event_hour': datetime.now().hour
        }
    
    def generate_purchase_event(self):
        """Génère un événement d'achat"""
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(10, 500), 2)
        
        return {
            'transaction_id': f"txn_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            'user_id': random.choice(USERS),
            'product_id': random.choice(PRODUCTS),
            'category': random.choice(CATEGORIES),
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': round(quantity * unit_price, 2),
            'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
            'timestamp': int(time.time() * 1000),
            'status': random.choice(['completed', 'pending', 'failed']),
            'event_date': datetime.now().strftime('%Y-%m-%d'),
            'event_hour': datetime.now().hour
        }
    
    def generate_inventory_event(self):
        """Génère un événement de stock"""
        return {
            'product_id': random.choice(PRODUCTS),
            'category': random.choice(CATEGORIES),
            'stock_level': random.randint(0, 1000),
            'reorder_level': 50,
            'warehouse_id': f"WH_{random.randint(1, 5):02d}",
            'timestamp': int(time.time() * 1000),
            'last_updated': datetime.now().isoformat(),
            'status': random.choice(['in_stock', 'low_stock', 'out_of_stock'])
        }
    
    def send_event(self, topic, event):
        """Envoie un événement vers Kafka"""
        try:
            future = self.producer.send(topic, event)
            future.get(timeout=10)
            return True
        except Exception as e:
            print(f"✗ Erreur envoi vers {topic}: {e}")
            return False
    
    def generate_realistic_stream(self, duration_seconds=600, events_per_second=10):
        """Génère un flux réaliste d'événements"""
        print(f"\n🚀 Génération de données pendant {duration_seconds}s ({events_per_second} événements/sec)")
        print(f"Topics: {list(TOPICS.values())}")
        print("-" * 80)
        
        start_time = time.time()
        total_events = {'clicks': 0, 'purchases': 0, 'inventory': 0}
        
        try:
            while (time.time() - start_time) < duration_seconds:
                iteration_start = time.time()
                
                for _ in range(events_per_second):
                    # 70% clics, 20% achats, 10% inventaire
                    rand = random.random()
                    
                    if rand < 0.7:
                        event = self.generate_click_event()
                        if self.send_event(TOPICS['clicks'], event):
                            total_events['clicks'] += 1
                    
                    elif rand < 0.9:
                        event = self.generate_purchase_event()
                        if self.send_event(TOPICS['purchases'], event):
                            total_events['purchases'] += 1
                    
                    else:
                        event = self.generate_inventory_event()
                        if self.send_event(TOPICS['inventory'], event):
                            total_events['inventory'] += 1
                
                # Affichage progression
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0 and elapsed > 0:
                    print(f"[{elapsed}s] Clics: {total_events['clicks']} | "
                          f"Achats: {total_events['purchases']} | "
                          f"Stock: {total_events['inventory']}")
                
                # Maintenir le rythme
                sleep_time = max(0, 1 - (time.time() - iteration_start))
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            print("\n⚠ Arrêt demandé par l'utilisateur")
        
        finally:
            print("\n" + "=" * 80)
            print("📊 RÉSUMÉ FINAL:")
            print(f"  • Clics générés: {total_events['clicks']}")
            print(f"  • Achats générés: {total_events['purchases']}")
            print(f"  • Événements stock: {total_events['inventory']}")
            print(f"  • TOTAL: {sum(total_events.values())} événements")
            print("=" * 80)
            
            if self.producer:
                self.producer.flush()
                self.producer.close()
                print("✓ Producteur Kafka fermé")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║  GÉNÉRATEUR DE DONNÉES E-COMMERCE - BIG DATA PROJECT    ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    generator = EcommerceDataGenerator()
    
    # Générer pendant 5 minutes (300s) à 10 événements/seconde
    # Total: ~3000 événements
    generator.generate_realistic_stream(duration_seconds=600, events_per_second=10)

if __name__ == "__main__":
    main()
