from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

class KafkaHelper:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
    
    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self.admin_client.create_topics(new_topics=[topic], validate_only=False)
            print(f"Topic '{topic_name}' created.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists.")
    
    def get_consumer(self, topic_name, group_id=None, auto_offset_reset='earliest'):
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset
        )
        return consumer
    
    def send_message(self, topic_name, message):
        self.producer.send(topic_name, value=message.encode('utf-8'))
        self.producer.flush()
        print(f"Message sent to topic '{topic_name}': {message}")

    def close(self):
        self.producer.close()
        self.admin_client.close()