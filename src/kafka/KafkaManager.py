from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

class KafkaManager:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        self._producer = None  # Initialize shared producer instance
        self._consumer = None  # Initialize shared consumer instance

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self.admin_client.create_topics(new_topics=[topic], validate_only=False)
            print(f"Topic '{topic_name}' created.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists.")

    def get_consumer(self, topic_name, group_id=None, auto_offset_reset='earliest'):
        if self._consumer is None:
            self._consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset=auto_offset_reset
            )
        return self._consumer

    def get_producer(self):
        if self._producer is None:
            self._producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return self._producer

    def send_message(self, topic_name, message):
        producer = self.get_producer()
        try:
            producer.send(topic_name, value=message.encode('utf-8'))
            producer.flush()
            print(f"Message sent to topic '{topic_name}': {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def close(self):
        if self._producer is not None:
            self._producer.close()
        if self._consumer is not None:
            self._consumer.close()
        self.admin_client.close()