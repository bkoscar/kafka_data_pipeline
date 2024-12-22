import json
from kafka import KafkaProducer
import socket

def main():
    producer = KafkaProducer(
        bootstrap_servers='kafka:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Connect to the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('sensor_container', 5555))

    buffer = ""
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                sensor_data = json.loads(line)
                producer.send('sensor_data', value=sensor_data)
                print(f"Datos enviados a Kafka: {sensor_data}")
        except Exception as e:
            print(f"Error al conectar o enviar datos: {e}")
            break

if __name__ == "__main__":
    main()