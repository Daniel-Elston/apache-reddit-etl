from __future__ import annotations

import json

from kafka import KafkaConsumer

from config import my_vars

CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC = my_vars()

# Initialize Kafka consumer


def listen_to_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER_URL],
        auto_offset_reset='latest',  # earliest
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Consume messages
    for message in consumer:
        print(f"Received message: {message.value}")

        with open(f'data/temp/{KAFKA_TOPIC}.json', 'a') as f:
            json.dump(message.value, f, indent=4)
            f.write('\n')


if __name__ == '__main__':
    listen_to_messages()
