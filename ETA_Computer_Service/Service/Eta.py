from kafka import KafkaConsumer, KafkaProducer
import random, datetime, threading, json, time, logging

__product__ = "Eta Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "2.0"
__maintainer__ = "Duminy Gaetan"
__email__ = "gaetan.duminy@etu.unice.fr"
__status__ = "development"

queue = []

class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['eta'])
        global queue
        
        for message in consumer:
            jsonFile = message.value
            if jsonFile['action'] == "eta_requested":
                body = jsonFile['message']
                time1 = random.randint(10, 20)
                time2 = time1 + random.randint(5, 15)
                date = datetime.datetime.now()
                data = {"action": "eta_response", "message":
                {    "id_request": body['id_request'],
                     "restaurant": body['restaurant'],
                     "meal": body['meal'],
                     "delivery_address": body['delivery_address'],
                     "pick_up_date": str(date + datetime.timedelta(minutes=time1)),
                     "delivery_date": str(date + datetime.timedelta(minutes=time2))
                }}
                queue.append(data)
            
class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        global queue
        while True:
            if len(queue) > 0:
                producer.send('eta', queue.pop())

def main():
    threads = [
        Consumer(),
        Producer()
    ]

    for t in threads:
        t.start()

    while True : time.sleep(60)
    
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
