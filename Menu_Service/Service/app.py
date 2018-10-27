#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os
import signal
import sys
import threading
import time
import logging

import pymysql
from jsonify.convert import jsonify

from kafka import KafkaProducer

__product__ = "Menu Service"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nikita Rousseau"]
__license__ = "MIT"
__version__ = "2.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"

# APPLICATION RUNTIME ENVIRONMENT
# (production|development)
env = 'development'

# GLOBAL VARIABLE
g = None
# GLOBAL THREAD REGISTRY
threads = []
# CLEAN EXIT FUNCTION
t_stop_event = threading.Event()


def __sigint_handler(signal, frame):
    """
    Catch CTR+C / KILL signals
    Do housekeeping before leaving
    """
    logging.debug("SIGINT or SIGTERM catched")
    logging.debug("Raise t_stop_event")
    t_stop_event.set()  # Set stop flag to true for all launched threads
    logging.debug("Stopping daemons...")


signal.signal(signal.SIGINT, __sigint_handler)
signal.signal(signal.SIGTERM, __sigint_handler)


def __load_config():
    """
    Parse database configuration file
    """
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config


def before_request():
    # DATABASE CONNECTION
    g.database_handle = None

    # LOAD CONFIGURATION
    db_config = __load_config()[env]

    try:
        # Connect to the database
        g.database_handle = pymysql.connect(host=db_config['host'],
                                            port=int(db_config['port']),
                                            user=db_config['user'],
                                            password=db_config['pass'],
                                            db=db_config['db'],
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor,
                                            autocommit=True,
                                            connect_timeout=60)
    except pymysql.err.OperationalError:
        logging.debug('Cannot process request : unable to connect to the database !')
        logging.debug('Maybe the `docker-compose` is not ready ?')
        print("Cannot process request : unable to connect to the database. Maybe the `docker-compose` is not ready ?")
        return jsonify({
            'status': 'KO',
            'message': "Unable to connect to the database. Maybe the `docker-compose` is not ready ?"
        }), 500


def after_request():
    # DISCONNECT FROM THE DATABASE
    if g.database_handle:
        g.database_handle.close()


# THREAD WORKERS

def kafka_producer_worker(topic):
    while not t_stop_event.is_set():
        print("produce " + topic)
        time.sleep(10)
        print("loop0")
    return


def kafka_consumer_worker(topic):
    while not t_stop_event.is_set():
        print("consume " + topic)
        time.sleep(15)
        print("loop1")
    return


"""
# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test',
                         bootstrap_servers=['mint-virtual-machine:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

producer = KafkaProducer(bootstrap_servers='mint-virtual-machine:9092', acks='all')
for _ in range(10):
    producer.send('test', b'some_message_bytes')

producer.flush()
"""


# MAIN

if __name__ == "__main__":
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'production':
        env = 'production'

    # LOGGING
    if env == 'production':
        logging.basicConfig(
            filename='app-production.log',
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            filename='app-development.log',
            level=logging.DEBUG
        )

    # PRODUCER
    t_producer_worker = threading.Thread(
        name='kafka_producer_worker',
        daemon=True,
        target=kafka_producer_worker,
        args=('toto',)
    )
    threads.append(t_producer_worker)

    # CONSUMER
    t_kafka_consumer_worker = threading.Thread(
        name='kafka_consumer_worker',
        daemon=True,
        target=kafka_consumer_worker,
        args=('titi',)
    )
    threads.append(t_kafka_consumer_worker)

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
