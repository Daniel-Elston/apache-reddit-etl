from __future__ import annotations

import json

from kafka import KafkaConsumer

from config import my_vars

CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC = my_vars()

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='latest',  # earliest
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

# Consume messages
for message in consumer:
    print(f"Received message: {message.value}")
