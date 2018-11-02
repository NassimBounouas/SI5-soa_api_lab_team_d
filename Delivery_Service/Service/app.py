#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import json
import os
import signal
import sys
import threading
import queue
import logging
import pymysql
from time import sleep
from kafka import KafkaProducer
from kafka import KafkaConsumer

__product__ = "Delivery Service"
__author__ = "Nassim Bounouas"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nassim Bounouas", "Nikita Rousseau"]
__license__ = "MIT"
__version__ = "2.0"
__maintainer__ = "Nassim BOUNOUAS"
__email__ = "nassim.bounouas@etu.unice.fr"
__status__ = "development"

# TODO : implement factory / database service in order to reduce coupling with database handle

# APPLICATION RUNTIME ENVIRONMENT
# (production|development)
env = 'development'
# GLOBAL APPLICATION CONFIGURATION
app_config = []
bootstrap_servers = ()
# GLOBAL THREAD REGISTRY
threads = []
# CLEAN EXIT EVENT
t_stop_event = threading.Event()


def __sigint_handler(signal, frame):
    """
    Catch CTR+C / KILL signals
    Do housekeeping before leaving
    """
    logging.debug("SIGINT or SIGTERM catched")
    logging.debug("Raise t_stop_event")
    t_stop_event.set()  # Set stop flag to true for all launched threads
    logging.info("Stopping daemons...")
    sleep(1)


signal.signal(signal.SIGINT, __sigint_handler)
signal.signal(signal.SIGTERM, __sigint_handler)


def __load_config(runtime_env):
    """
    Parse database configuration file
    :string runtime_env: (production|development)
    """
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    _app_config = configparser.ConfigParser()
    _app_config.read(config_file)

    # Evaluate
    _app_config = _app_config[runtime_env]
    return _app_config


# DATABASE HELPERS


def __mysql_connect():
    global app_config

    return pymysql.connect(host=app_config['host'],
                           port=int(app_config['port']),
                           user=app_config['user'],
                           password=app_config['pass'],
                           db=app_config['db'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor,
                           autocommit=True,
                           connect_timeout=60)


def __mysql_close(database_handle=None):
    if database_handle:
        database_handle.close()


def __populate_db():
    from model.order import Order
    dbh = __mysql_connect()

    # Meals
    Order(dbh=dbh, meal_name="testmeal", pickup_restaurant="testrestaurant", pickup_date="2018-11-02 12:00", delivery_address="testdeliveryaddress")

    __mysql_close(dbh)


# BUSINESS FUNCTIONS


def save_order(dbh,meal_name, pickup_restaurant, pickup_date, delivery_address):
    from model.order import Order
    Order(dbh=dbh, meal_name=meal_name, pickup_restaurant=pickup_restaurant, pickup_date=pickup_date,
          delivery_address=delivery_address)

# THREAD WORKERS

def kafka_delivery_producer_worker(mq: queue.Queue):
    """
    Kafka Delivery Topic Producer
    as thread worker
    Get messages from a shared mq queue.Queue
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda item: json.dumps(item).encode('utf-8'))

    while not t_stop_event.is_set():
        try:
            if mq.qsize() > 0:
                # Topic + Message
                msg = mq.get()
                logging.info("GET %s FROM QUEUE AND SENDING TO %s" % (msg, 'delivery'))
                producer.send('delivery', msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return


def kafka_delivery_consumer_worker(mq: queue.Queue):
    """
    Kafka Delivery Topic Consumer
    as thread worker
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer = KafkaConsumer('delivery',
                             bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda item: json.loads(item.decode('utf-8')))

    while not t_stop_event.is_set():
        try:
            # Message loop
            for message in consumer:
                logging.info("READING MESSAGE %s:%d:%d: key=%s value=%s" % (
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    message.value)
                )

                # simple sanitizer
                if ('action' not in message.value) \
                        or ('message' not in message.value) \
                        or ('request' not in message.value['message']):
                    logging.info("MALFORMED MESSAGE value=%s SKIPPING" % (message.value,))
                    continue

                # Pre routine
                dbh = __mysql_connect()

                # Action switch
                if str(message.value["action"]).upper() == "DELIVERY_REQUEST":
                    logging.info("SAVING A NEW ORDER")
                    save_order(
                            dbh,
                            message.value["message"]["meal_name"],
                            message.value["message"]["pickup_restaurant"],
                            message.value["message"]["pickup_date"],
                            message.value["message"]["delivery_address"]
                    )

                # Post routine
                __mysql_close(dbh)
        except pymysql.err.OperationalError:
            logging.error('Cannot process request : unable to connect to the database !')
            logging.error('Maybe the `docker-compose` is not ready ?')
        except Exception as e:
            logging.fatal(e, exc_info=True)

    consumer.close()
    return


# MAIN

if __name__ == "__main__":
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'production':
        env = 'production'

    # LOGGING
    if env == 'production':
        logging.basicConfig(
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            level=logging.INFO
        )

    # CONFIGURATION
    app_config = __load_config(env)
    if ',' in str(app_config['bootstrap_servers']):
        bootstrap_servers = list(filter(None, str(app_config['bootstrap_servers']).split(',')))
    else:
        bootstrap_servers = str(app_config['bootstrap_servers'])

    # Init DB
    __populate_db()

    # DELIVERY CONSUMER
    delivery_mq = queue.Queue()  # Shared queue between consumer / producer threads

    t_kafka_delivery_consumer_worker = threading.Thread(
        name='kafka_consumer_worker',
        daemon=True,
        target=kafka_delivery_consumer_worker,
        args=(delivery_mq,)
    )
    threads.append(t_kafka_delivery_consumer_worker)

    # PRODUCER
    t_producer_worker = threading.Thread(
        name='kafka_producer_worker',
        daemon=True,
        target=kafka_delivery_producer_worker,
        args=(delivery_mq,)
    )
    threads.append(t_producer_worker)

    # Start
    logging.info('Starting...')
    # Starting threads
    for t in threads:
        t.start()

    logging.info('Ready !')
    logging.info('Serving application in `' + env + '` environment')
    # Waiting threads...
    for t in threads:
        t.join()

    logging.info('Bye !')
    exit(0)
