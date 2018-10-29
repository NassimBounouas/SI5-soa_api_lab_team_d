from kafka import KafkaConsumer,KafkaProducer
import random
import pymysql
import configparser
import threading
import json
import time
import os


global db
global connected
queue =[]


def load_config():
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config

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
    data =  {
        "Action" : "PREPARE_COMMANDE",
        "Message" : {
            'id request' : ID,
            'id restaurant' : jsonRecv["id restaurant"],
            'id meal' : jsonRecv["id meal"]
                }
    }
    databaseAddRecipe(jsonRecv,ID)
    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

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
            "Action" : "PREPARE_COMMAND",
            "Message" :
                {
                    'id_request' : res[0]['id_request'],
                    'id_restaurant' : res[0]['id_restaurant'],
                    'id_meal' : res[0]['id_meal']
                }
        }
    else:
        return json.loads('{Message = "No Command in the database",Status = "Refused"}')
    
    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

class connect_kafka_producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v:
                                 json.dumps(v).encode('utf-8'))
        global queue
        while True:
            if len(queue) > 0:
                producer.send('restaurant', queue.pop())
                time.sleep(1)

class connect_kafka_consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(
            bootstrap_servers = 'localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['ordering'])
        for jsonMessage in consumer:
            before_request()
            if jsonMessage.value["Action"] == "ORDER_REQUEST":
                queue.append(validateOrder(jsonMessage.value["Message"]))
            elif jsonMessage.value["Action"] == "VALIDATE_ORDER":
                queue.append(databaseReadRecipe(jsonMessage.value["Message"]["Id"]))
            else:
                queue.append(json.loads('{error = "404 Not Found")}'))
            after_request()


def main():
    threads = [
        connect_kafka_producer(),
        connect_kafka_consumer()]
    for t in threads:
        t.start()
    time.sleep(10)

if __name__ == '__main__':
    main()
