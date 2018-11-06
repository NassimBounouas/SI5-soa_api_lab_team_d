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

from business.create_order import create_order
from business.prepare_order import prepare_order
from business.validate_order import validate_order
from business.get_order_list import get_order_list

__product__ = "Ordering Service"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Rudy Meersman", "Nikita Rousseau"]
__license__ = "MIT"
__version__ = "2.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"

# APPLICATION RUNTIME ENVIRONMENT
# (production|development)
env = 'development'
# GLOBAL APPLICATION CONFIGURATION
app_config = []
bootstrap_servers = []
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


# THREAD WORKERS

def kafka_producer_worker(topic: str, mq: queue.Queue):
    """
    Kafka Generic Message Producer
    as thread worker
    Get messages from a shared mq queue.Queue
    :param topic: str
    :param mq: queue.Queue
    :return:
    """
    # Client
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda item: json.dumps(item).encode('utf-8'))

    while not t_stop_event.is_set():
        # 10ms
        sleep(0.01)
        try:
            if mq.qsize() > 0:
                # Topic + Message
                msg = mq.get()
                logging.info("GET %s AND SENDING TO %s" % (msg, topic))
                producer.send(topic, msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return


def kafka_restaurant_consumer_worker(ordering_mq: queue.Queue, restaurant_mq: queue.Queue):
    """
    Kafka Restaurant Topic Consumer
    as thread worker
    :param ordering_mq: queue.Queue
    :param restaurant_mq: queue.Queue
    :return:
    """
    global app_config
    consumer_restaurant = KafkaConsumer('restaurant',
                                    bootstrap_servers=bootstrap_servers,
                                    value_deserializer=lambda item: json.loads(item.decode('utf-8')))
    while not t_stop_event.is_set():
        try:
            # Message loop
            for message in consumer_restaurant:
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
                if str(message.value["action"]).upper() == "ORDER_LIST_REQUEST":
                    logging.info("PUT get_order_list MESSAGE in QUEUE")
                    restaurant_mq.put(
                        get_order_list(
                            dbh,
                            int(message.value["message"]["request"]),
                            message.value["message"]
                        )
                    )
                # Post routine
                __mysql_close(dbh)
        except pymysql.err.OperationalError:
            logging.error('Cannot process request : unable to connect to the database !')
            logging.error('Maybe the `docker-compose` is not ready ?')
        except Exception as e:
            logging.fatal(e, exc_info=True)
    consumer_restaurant.close()
    return

def kafka_ordering_consumer_worker(ordering_mq: queue.Queue, restaurant_mq: queue.Queue):
    """
    Kafka Ordering Topic Consumer
    as thread worker
    :param ordering_mq: queue.Queue
    :param restaurant_mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer_ordering = KafkaConsumer('ordering',
                             bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda item: json.loads(item.decode('utf-8')))
    while not t_stop_event.is_set():
        try:
            # Message loop
            for message in consumer_ordering:
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
                if str(message.value["action"]).upper() == "RESTAURANT_ORDER_REQUEST":
                    logging.info("PUT create_order MESSAGE in QUEUE")
                    ordering_mq.put(
                        create_order(
                            dbh,
                            int(message.value["message"]["request"]),
                            message.value["message"]
                        )
                    )
                elif str(message.value["action"]).upper() == "VALIDATE_ORDER_REQUEST":
                    logging.info("PUT validate_order MESSAGE in QUEUE")
                    # notify restaurant
                    restaurant_mq.put(
                        prepare_order(
                            dbh,
                            int(message.value["message"]["request"]),
                            message.value["message"]
                        )
                    )
                    # update order status as accepted
                    ordering_mq.put(
                        validate_order(
                            dbh,
                            int(message.value["message"]["request"]),
                            message.value["message"]
                        )
                    )
                # Post routine
                __mysql_close(dbh)
        except pymysql.err.OperationalError:
            logging.error('Cannot process request : unable to connect to the database !')
            logging.error('Maybe the `docker-compose` is not ready ?')
        except Exception as e:
            logging.fatal(e, exc_info=True)
    consumer_ordering.close()
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
        bootstrap_servers.append(str(app_config['bootstrap_servers']))

    ###########################################################

    # RESTAURANT TOPIC I/O
    restaurant_mq = queue.Queue()
    ordering_mq = queue.Queue()

    # CONSUMERS
    t_consumer_ordering_worker = threading.Thread(
        name='kafka_ordering_consumer_worker',
        daemon=True,
        target=kafka_ordering_consumer_worker,
        args=(ordering_mq, restaurant_mq,)
    )
    threads.append(t_consumer_ordering_worker)

    t_consumer_restaurant_worker = threading.Thread(
        name='kafka_restaurant_consumer_worker',
        daemon=True,
        target=kafka_restaurant_consumer_worker,
        args=(ordering_mq, restaurant_mq,)
    )
    threads.append(t_consumer_restaurant_worker)

    # PRODUCERS
    t_restaurant_producer_worker = threading.Thread(
        name='kafka_restaurant_producer_worker',
        daemon=True,
        target=kafka_producer_worker,
        args=('restaurant', restaurant_mq,)
    )
    threads.append(t_restaurant_producer_worker)
    t_ordering_producer_worker = threading.Thread(
        name='kafka_ordering_producer_worker',
        daemon=True,
        target=kafka_producer_worker,
        args=('ordering', ordering_mq,)
    )
    threads.append(t_ordering_producer_worker)

    ###########################################################

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
