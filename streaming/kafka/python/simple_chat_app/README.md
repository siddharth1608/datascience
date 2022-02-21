# Simple Chat application in Kafka using Python

  

### Steps

#### Step 1: Run Zookeeper service
From the folder where you extracted kafka run the following command
>$ bin/zookeeper-server-start.sh config/zookeeper.properties

#### Step 2: Run Kafka server
In another terminal, execute this script
>$ bin/kafka-server-start.sh config/server.properties

#### Step 3: Create Kafka Consumer

In a new terminal, run the consumer script
>$ python kafka-consumer.py

Code present here - [kafka-consumer.py](https://github.com/siddharth1608/datascience/blob/master/streaming/kafka/python/simple_chat_app/kafka-consumer.py)
 
#### Step 4: Create Kafka Producer
Again in another terminal, execute producer script and type a message & hit Enter. The message from this terminal will instantly appear in consumer terminal started in the previous step
>$ python producer.py

Code present here - [kafka-producer.py](https://github.com/siddharth1608/datascience/blob/master/streaming/kafka/python/simple_chat_app/kafka-producer.py)

**Note**: I have created the topic inside the Producer code. We can also do that in the terminal after Step 2 above using the following command
>bin/kafka-topics.sh --describe --topic simple-chat-app --bootstrap-server localhost:9092