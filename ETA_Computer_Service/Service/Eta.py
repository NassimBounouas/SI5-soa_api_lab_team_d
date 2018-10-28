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
            print(type(jsonFile))
            if jsonFile['Action'] == "ETA_REQUESTED":
                body = jsonFile['Message']
                time1 = random.randint(10, 20)
                time2 = time1 + random.randint(5, 15)
                date = datetime.datetime.now()
                data = {"Action": "ETA_RESPONSE", "Message":
                {    "ID_Request": body['ID_Request'],
                     "Restaurant": body['Restaurant'],
                     "Meal": body['Meal'],
                     "Delivery_Address": body['Delivery_Address'],
                     "Pick_Up_Date": str(date + datetime.timedelta(minutes=time1)),
                     "Delivery_Date": str(date + datetime.timedelta(minutes=time2))
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
                test= queue.pop();
                print(type(test))
                producer.send('eta', test)

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
