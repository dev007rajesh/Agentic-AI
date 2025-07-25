import time
import threading
from kafka import KafkaConsumer
# Assuming you have a config setup, replace with your actual config loading
# For now, we'll use a simple dictionary for configuration
class Config:
    def get(self, *keys, default=None):
        # This is a placeholder, replace with your actual config loading logic
        config_data = {
            'kafka': {
                'consumers': {
                    'my_topic': {
                        'group_id': 'my_group',
                        'auto_offset_reset': 'earliest'
                    },
                    'another_topic': {
                        'group_id': 'another_group',
                        'auto_offset_reset': 'latest'
                    }
                },
                'polling_interval_seconds': 5
            }
        }
        
        data = config_data
        for key in keys:
            data = data.get(key, {})
            if data == {}:
                return default
        return data if data != {} else default

config = Config()

class KafkaConsumerManager:
    def __init__(self, kafka_manager):
        self.kafka_manager = kafka_manager
        self.consumers = []
        self.running = False
        self.consumer_threads = []

    def load_consumer_configs(self):
        # Load consumer configurations from your config source
        consumer_configs = config.get('kafka', 'consumers', {})
        return consumer_configs

    def start_consumers(self):
        consumer_configs = self.load_consumer_configs()
        for topic, settings in consumer_configs.items():
            consumer = self.kafka_manager.get_consumer(
                topic_name=topic,
                group_id=settings.get('group_id'),
                auto_offset_reset=settings.get('auto_offset_reset', 'earliest')
            )
            self.consumers.append(consumer)
            
            # Start a thread for each consumer's consumption loop
            consumer_thread = threading.Thread(target=self.run_consumption_loop, args=(consumer, topic))
            self.consumer_threads.append(consumer_thread)
            consumer_thread.start()

        self.running = True
        print("Kafka consumers started.")

    def run_consumption_loop(self, consumer, topic):
        print(f"Consumer started for topic: {topic}")
        while self.running:
            messages = consumer.poll(timeout_ms=1000) # Poll with a timeout
            if messages:
                for topic_partition, records in messages.items():
                    for record in records:
                        try:
                            # Process the message
                            self.process_message(record.value, topic)
                            consumer.commit() # Commit offset after successful processing
                        except Exception as e:
                            # Handle processing errors (logging, retries, etc.)
                            print(f"Error processing message from topic {topic}: {e}")
            time.sleep(config.get('kafka', 'polling_interval_seconds', 5)) # Configurable interval
        print(f"Consumer stopped for topic: {topic}")

    def process_message(self, message, topic):
        # Implement your message processing logic here
        print(f"Received message from topic {topic}: {message}")

    def stop_consumers(self):
        print("Stopping Kafka consumers...")
        self.running = False
        for consumer in self.consumers:
            consumer.close()
        for thread in self.consumer_threads:
            thread.join() # Wait for consumer threads to finish
        print("Kafka consumers stopped.")
