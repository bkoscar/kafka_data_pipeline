import random
import time
import json
import socket
import threading
from datetime import datetime, timedelta

# Add batch configuration
BATCH_SIZE = 100  # readings per second
NOISE_FACTOR = 0.1  # 10% variation
# Define sensor types and their ranges
SENSORS = {
    'temperature': {'min': -10, 'max': 40, 'unit': 'C'},
    'humidity': {'min': 0, 'max': 100, 'unit': '%'},
    'pressure': {'min': 980, 'max': 1050, 'unit': 'hPa'},
    'co2': {'min': 400, 'max': 2000, 'unit': 'ppm'},
    'light': {'min': 0, 'max': 100000, 'unit': 'lux'}
}


def generate_sensor_batch():
    batch = []
    base_time = datetime.now()
    
    for i in range(BATCH_SIZE):
        timestamp = (base_time + timedelta(milliseconds=i*10)).isoformat()
        readings = {}
        
        for sensor, ranges in SENSORS.items():
            # Add noise
            base_value = random.uniform(ranges['min'], ranges['max'])
            noise = random.uniform(-NOISE_FACTOR, NOISE_FACTOR) * base_value
            value = round(base_value + noise, 2)
            
            readings[sensor] = {
                'value': value,
                'unit': ranges['unit']
            }
        
        batch.append({
            'timestamp': timestamp,
            'readings': readings
        })
    
    return batch

def handle_client(client_socket):
    try:
        while True:
            batch = generate_sensor_batch()
            for data in batch:
                message = json.dumps(data) + "\n"
                client_socket.send(message.encode())
            time.sleep(1)  # Send batch every second
    except:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server started on port 5555")

    try:
        while True:
            client, addr = server.accept()
            print(f"Client connected from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.daemon = True
            client_handler.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()

if __name__ == "__main__":
    main()