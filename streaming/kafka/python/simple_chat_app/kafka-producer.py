from kafka import KafkaProducer, KafkaConsumer, KafkaClient

print("Kafka Producer")

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# def produce_number_seq(max_number):    
#     for i in range(max_number):
#         producer.send('test', b"number %d" % i)    
#     producer.flush()

#max_number = int(input("Enter a maximum number"))    
#produce_number_seq(max_number)
    
def transfer_message(text):
    """
    This function will accept user input text and broadcast it to the Kafka topic
    """
    producer.send('test', text.encode('utf-8'))
    
    producer.flush()
    
print("Type your message and hit Enter")

while(True):
    msg = input()
    transfer_message(msg)