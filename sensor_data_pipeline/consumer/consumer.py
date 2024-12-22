import json
from kafka import KafkaConsumer

def main():
    consumer = KafkaConsumer(
        'sensor_data',
        bootstrap_servers='kafka:29092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='sensor-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        sensor_data = message.value
        print(f"Datos recibidos de Kafka: {sensor_data}")

if __name__ == "__main__":
    main()