from kafka import KafkaConsumer, KafkaProducer
import threading, json, time, logging

__product__ = "Paywall Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Duminy Gaetan"
__email__ = "gaetan.duminy@etu.unice.fr"
__status__ = "development"

queue = []

def checkValidity(Card_Number, Shipping_Address):
    return True

def credit_deliverer(ID_Order, ID_Coursier, Amount):
    return 0

class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['ordering'])
        consumer.subscribe(['payment'])
        
        global queue
        
        for message in consumer:
            jsonFile = message.value
            print(type(jsonFile))
            if jsonFile['action'] == "payment_placed":
                body = jsonFile['message']
                if checkValidity(jsonFile['message']['card_number'], jsonFile['message']['shipping_address']) :
                    data = {"action": "payment_accepted", "message":
                             {    "id_request": body['id_request']
                             }}
                    queue.append(data)
            if jsonFile['action'] == "notify_delivery_response":
                body = jsonFile['message']
                credit_deliverer(jsonFile['message']['id_order'], jsonFile['message']['id_coursier'], jsonFile['message']['amount'])
                print("Ok")
            
class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer_ordering = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        global queue
        while True:
            if len(queue) > 0:
                test= queue.pop();
                print(type(test))
                producer_ordering.send('ordering', test)

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
