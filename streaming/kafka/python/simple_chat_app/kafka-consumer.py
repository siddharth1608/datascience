from kafka import KafkaProducer, KafkaConsumer, KafkaClient

print("Kafka Consumer")

consumer = KafkaConsumer('simple-chat-app',bootstrap_servers='localhost:9092')
for msg in consumer:
    print(msg.value.decode('utf-8')) 