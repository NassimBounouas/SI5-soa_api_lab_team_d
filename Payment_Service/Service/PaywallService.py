#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import threading
import json
import signal
import sys
import queue
import logging
import os
import configparser
from time import sleep
from kafka import KafkaConsumer
from kafka import KafkaProducer

__product__ = "Paywall Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Duminy Gaetan"
__email__ = "gaetan.duminy@etu.unice.fr"
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


# BUSINESS FUNCTIONS


def check_validity(request_id):
    return {
        "action": "PAYMENT_ACCEPTED",
        "message": {
            "status": "OK",
            "request": int(request_id)
        }
    }

def credit_deliverer():
    return True


# THREAD WORKERS


def kafka_ordering_producer_worker(mq: queue.Queue):
    """
    Kafka Ordering Topic Producer
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
                logging.info("GET %s FROM QUEUE AND SENDING TO %s" % (msg, 'ordering'))
                producer.send('ordering', msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return

def kafka_ordering_consumer_worker(mq: queue.Queue):
    """
    Kafka Ordering Topic Consumer
    as thread worker
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer = KafkaConsumer('ordering',
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest',
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
                if ("action" not in message.value) \
                        or ("message" not in message.value) \
                        or ("request" not in message.value["message"]):
                    logging.info("MALFORMED MESSAGE value=%s SKIPPING" % (message.value,))
                    continue

                # Action switch
                if str(message.value["action"]).upper() == "PAYMENT_PLACED":
                    logging.info("PUT check_validity MESSAGE in QUEUE")
                    mq.put(
                        check_validity(message.value["message"]["request"])
                    ) 
        except Exception as e:
            logging.fatal(e, exc_info=True)
    # Post routine

    consumer.close()
    return
            
def kafka_payment_consumer_worker(mq: queue.Queue):
    """
    Kafka Payment Topic Consumer
    as thread worker
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer = KafkaConsumer('payment',
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest',
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
                if ("action" not in message.value) \
                        or ("message" not in message.value) \
                        or ("request" not in message.value["message"]):
                    logging.info("MALFORMED MESSAGE value=%s SKIPPING" % (message.value,))
                    continue

                # Action switch
                if str(message.value["action"]).upper() == "NOTIFY_DELIVERY_RESPONSE":
                    logging.info("MESSAGE <NOTIFY_DELIVERY_RESPONSE> RECEIVE") # Mocked
                    """logging.info("PUT credit_deliverer MESSAGE in QUEUE")
                    mq.put(
                        credit_deliverer()
                    )"""
        except Exception as e:
            logging.fatal(e, exc_info=True)
    # Post routine

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
        bootstrap_servers.append(str(app_config['bootstrap_servers']))

    # QUEUES
    ordering_mq = queue.Queue()  # Shared queue between consumer / producer threads
    payment_mq = queue.Queue()

    # CONSUMERS

    t_kafka_ordering_consumer_worker = threading.Thread(
        name='kafka_ordering_consumer_worker',
        daemon=True,
        target=kafka_ordering_consumer_worker,
        args=(ordering_mq,)
    )
    threads.append(t_kafka_ordering_consumer_worker)

    t_kafka_payment_consumer_worker = threading.Thread(
        name='kafka_payment_consumer_worker',
        daemon=True,
        target=kafka_payment_consumer_worker,
        args=(payment_mq,)
    )
    threads.append(t_kafka_payment_consumer_worker)

    # PRODUCER
    t_ordering_producer_worker = threading.Thread(
        name='kafka_ordering_producer_worker',
        daemon=True,
        target=kafka_ordering_producer_worker,
        args=(ordering_mq,)
    )
    threads.append(t_ordering_producer_worker)

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
