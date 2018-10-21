from flask import Flask, request, jsonify,g
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
#app = Flask(__name__)


def load_config():
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config

#@app.before_request
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

#@app.after_request
def after_request():
    global connected
    global db
    if connected:
        db.close()
        print("Database closed.")
    connected = False
    return

def orderMeal(jsonRecv):
    data = {"Action" : "compute_eta",
            "Message" : databaseReadRestaurant(jsonRecv["Meal"]) }
    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

def validateOrder(jsonRecv):
    ID = random.randint(0,100)
    data =  { "Message" : {
                'Command_Id' : ID,
                'Restaurant' : jsonRecv["Restaurant"],
                'Meal' : jsonRecv["Meal"],
                'Delivery_Address' : jsonRecv["Delivery_Address"],
                'Delivery_Date' : jsonRecv["Delivery_Date"]
                },
                "Status" : "Accepted" }
    databaseAddRecipe(jsonRecv)
    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

def databaseAddRecipe(jsonRecv):
    global db
    cursor = db.cursor()
    sql = "INSERT INTO to_get_recipe(meal_name,restaurant_name,delivery_date,delivery_address,price) VALUES('%s','%s','%s','%s','%d')" %(jsonRecv["Meal"],jsonRecv["Restaurant"],jsonRecv["Delivery_Date"],jsonRecv["Delivery_Address"],jsonRecv["Price"])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    return

def databaseReadRecipe(identifier):
    global db
    cursor = db.cursor()
    sql = ("SELECT * FROM to_get_recipe WHERE id=" + str(identifier))
    try:
        cursor.execute(sql)
    except:
        db.rollback()
    res = cursor.fetchall()
    if len(res) > 0:
        data = { "Message" :
                {
                    'Command_Id' : res[0]['id'],
                    'Restaurant' : res[0]['restaurant_name'],
                    'Meal' : res[0]['meal_name'],
                    'Delivery_Address' : res[0]['delivery_address'],
                    'Delivery_Date' : res[0]['delivery_date'],
                    'Price' : res[0]['price']
                },
                "Status" : "Accepted"
        }
    else:
        return json.loads('{Message = "No Command in the database",Status = "Refused"}')

    return json.loads('{ Message = ' +data+ ',Status = "Accepted"}')
    return json.loads(json.dumps(data, indent=4, sort_keys=True,default=str))

def databaseReadRestaurant(meal):
    global db
    cursor = db.cursor()
    sql = "SELECT * FROM to_get_restaurant WHERE meal_name=%s"
    try:
        cursor.execute(sql,meal)
    except:
        db.rollback()
    res = cursor.fetchall()
    return {
        'Restaurant' : res[0]['restaurant_name'],
        'Meal' : meal,
        'Price': res[0]['price']
    }

class connect_kafka_producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v:
                                 json.dumps(v).encode('utf-8'))
        global queue
        while True:
            if len(queue) > 0:
                producer.send('ordering_send', queue.pop())
                time.sleep(1)

class connect_kafka_consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(
            bootstrap_servers = 'localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['ordering_recv'])
        for jsonMessage in consumer:
            before_request()
            if jsonMessage.value["Action"] == "validate_order":
                queue.append(validateOrder(jsonMessage.value["Message"]))
            elif jsonMessage.value["Action"] == "order_meal":
                queue.append(orderMeal(jsonMessage.value["Message"]))
            elif jsonMessage["Action"] == "validation_request":
                return databaseReadRecipe(jsonMessage.value["Message"]["Id"])
            else:
                queue.append(json.loads('{error = "404 Not Found")}'))

            after_request()

#@app.route('/receive_event',methods = ['POST'])
def main():
    threads = [
        connect_kafka_producer(),
        connect_kafka_consumer()]
    for t in threads:
        t.start()
    time.sleep(10)

if __name__ == '__main__':
    #app.run(debug=False, host='0.0.0.0')
    main()
