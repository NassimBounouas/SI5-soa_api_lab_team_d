from kafka import KafkaConsumer,KafkaProducer
import random
import pymysql
import configparser
import threading
import json
import queue
import logging
import time
import os


global db
global connected
queue_all =[]
app_config = []
threads = []
t_stop_event = threading.Event()


def load_config():
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    _app_config = configparser.ConfigParser()
    _app_config.read(config_file)
    return _app_config

def before_request():
    configuration = load_config()["production"]
    print("Will connect to : " + configuration['host'] + " on port : " + configuration['port'])
    global db
    global connected
    try:
        db = pymysql.connect(host=configuration['host'],
                               port=int(configuration['port']),
                               user=configuration['user'],
                               password=configuration['pass'],
                               db=configuration['db'],
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor,
                               autocommit=True,
                               connect_timeout=60)
        connected = True
        print("Connected to Database.")
    except  pymysql.err.OperationalError:
        connected = False
        print("Cannot process request : unable to connect to the database. Maybe the `docker-compose` is not ready...")
        return json.loads({
            'status': 'KO',
            'message': "Cannot process request : unable to connect to the database. Maybe the `docker-compose` is not ready..."
        }), 500

def after_request():
    global connected
    global db
    if connected:
        db.close()
        print("Database closed.")
    connected = False
    return

def validateOrder(jsonRecv):
    ID = random.randint(0,100)
    databaseAddRecipe(jsonRecv,ID)
    #print(data)
    return

def databaseAddRecipe(jsonRecv,ID):
    global db
    cursor = db.cursor()
    sql = "INSERT INTO to_get_recipe(id_request,id_meal,id_restaurant,client_name,client_address,command_statut) VALUES('%d','%s','%s','%s','%s','%s')" %(ID,jsonRecv["id meal"],jsonRecv["id restaurant"],jsonRecv["client name"],jsonRecv["client address"],'Waiting')
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return

def databaseChangeStatueOrder(identifier):
    global db
    cursor = db.cursor()
    sql = "UPDATE to_get_recipe SET command_statut = %s  WHERE id_request=%s" %("Accepted",str(identifier))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return

def databaseReadRecipe(identifier):
    global db
    cursor = db.cursor()
    sql = ("SELECT * FROM to_get_recipe WHERE id_request =" + str(identifier))
    try:
        cursor.execute(sql)
    except:
        db.rollback()
    res = cursor.fetchall()
    if len(res) > 0:
        data = {
            "action" : "prepare_commande",
            "message" :
                {
                    'id_request' : res[0]['id_request'],
                    'id_restaurant' : res[0]['id_restaurant'],
                    'id_meal' : res[0]['id_meal']
                }
        }
        #print(data)
    else:
        return json.loads('{Message = "No Command in the database",Status = "Refused"}')

    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

def connect_kafka_producer(mq : queue.Queue):
    global app_config
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v:
                                 json.dumps(v).encode('utf-8'))
    while not t_stop_event.is_set():
        try:
            if mq.qsize() > 0:
                msg = mq.get()
                producer.send('restaurant', msg)
                producer.flush()
        except Exception as e:
            logging.fatal(e,exc_info=True)
    producer.close()
    return

def connect_kafka_consumer(mq: queue.Queue):
    global app_config
    consumer = KafkaConsumer(
            bootstrap_servers = 'localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe(['ordering'])
    while not t_stop_event.is_set():
        try:
            for jsonMessage in consumer:
                before_request()
                #print(jsonMessage)
                if jsonMessage.value["action"] == "order_request":
                    validateOrder(jsonMessage.value["message"])
                elif jsonMessage.value["action"] == "validate_order":
                    mq.put(databaseReadRecipe(jsonMessage.value["message"]["id"]))
                else:
                    continue
                after_request()
        except Exception as e:
            logging.fatal(e,exc_info=True)

def main():
    global threads
    queue_order = queue.Queue()
    t_producer_worker =  threading.Thread(
        name='kafka_producer_server',
        daemon = True,
        target = connect_kafka_producer,
        args = (queue_order,)
    )
    threads.append(t_producer_worker)
    t_consumer_worker = threading.Thread(
    name = 'kafka_consumer_server',
    daemon = True,
    target= connect_kafka_consumer,
    args = (queue_order,))

    threads.append(t_consumer_worker)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

