from __future__ import annotations

import json

from kafka import KafkaConsumer

# from utils.file_handler import temp_store

# Kafka configuration
KAFKA_BROKER_URL = 'localhost:9092'
KAFKA_TOPIC = 'reddit_comments'

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
    # temp_store(message.value, 'data/temp/kafka-reddit_comments.json') # temp store
