#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime
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

__product__ = "Eta Service"
__author__ = "Duminy Gaetan"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Duminy Gaetan"]
__license__ = "MIT"
__version__ = "2.1"
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


def compute_eta(request, _from, to):
    """
    Compute Eta, eta is a simple random (simulated)
    :param request: int
    :param _from: str
    :param to: str
    :return: json
    """

    time = random.randint(10, 20)

    return {
        "action": "ETA_RESPONSE",
        "message": {
            "status": "OK",
            "request": int(request),
            "from": _from,
            "to": to,
            "eta": time
        }
    }

def update_eta(request, order, to, lastLatitude, lastLongitude, timestamp):
    """
    Update Eta, eta is a simple random (simulated)
    :param request: int
    :param order: int
    :param to: str
    :param lastLatitude: float
    :param lastLongitude: float
    :param timestamp: str
    :return: json
    """

    time = random.randint(1, 9)

    return {
        "action": "DELIVERY_LOCATION_STATUS",
        "message": {
            "status": "OK",
            "request": int(request),
            "id_order": int(order),
            "to": to,
            "lastLatitude": float(lastLatitude),
            "lastLongitude": float(lastLongitude),
            "timestamp": timestamp,
            "eta": time
        }
    }

# THREAD WORKERS


def kafka_eta_producer_worker(mq: queue.Queue):
    """
    Kafka Eta Topic Producer
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
                logging.info("GET %s FROM QUEUE AND SENDING TO %s" % (msg, 'eta'))
                producer.send('eta', msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return


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


def kafka_eta_consumer_worker(mq_eta: queue.Queue):
    """
    Kafka Eta Topic Consumer
    as thread worker
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer = KafkaConsumer('eta',
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
                if ("action" not in message.value) \
                        or ("message" not in message.value) \
                        or ("request" not in message.value["message"]):
                    logging.info("MALFORMED MESSAGE value=%s SKIPPING" % (message.value,))
                    continue

                # Action switch
                if str(message.value["action"]).upper() == "ETA_REQUEST":
                    logging.info("PUT compute_eta MESSAGE in QUEUE")
                    mq_eta.put(
                        compute_eta(
                            message.value["message"]["request"],
                            message.value["message"]["from"],
                            message.value["message"]["to"]
                        )
                    )
        except Exception as e:
            logging.fatal(e, exc_info=True)
    # Post routine

    consumer.close()
    return

def kafka_delivery_consumer_worker(mq_delivery: queue.Queue):
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
                if ("action" not in message.value) \
                        or ("message" not in message.value) \
                        or ("request" not in message.value["message"]):
                    logging.info("MALFORMED MESSAGE value=%s SKIPPING" % (message.value,))
                    continue

                # Action switch
                if str(message.value["action"]).upper() == "ETA_UPDATE_REQUESTED":
                    logging.info("PUT update_eta MESSAGE in QUEUE")
                    mq_delivery.put(
                        update_eta(
                            message.value["message"]["request"],
                            message.value["message"]["id_order"],
                            message.value["message"]["to"],
                            message.value["message"]["lastLatitude"],
                            message.value["message"]["lastLongitude"],
                            message.value["message"]["timestamp"]
                        )
                    )
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

    #QUEUES
    eta_mq = queue.Queue()  # Shared queue between consumer / producer threads
    delivery_mq = queue.Queue()

    # ETA CONSUMER
    t_kafka_eta_consumer_worker = threading.Thread(
        name='kafka_eta_consumer_worker',
        daemon=True,
        target=kafka_eta_consumer_worker,
        args=(eta_mq,)
    )
    threads.append(t_kafka_eta_consumer_worker)

    # DELIVERY CONSUMER
    t_kafka_delivery_consumer_worker = threading.Thread(
        name='kafka_delivery_consumer_worker',
        daemon=True,
        target=kafka_delivery_consumer_worker,
        args=(delivery_mq,)
    )
    threads.append(t_kafka_delivery_consumer_worker)

    # ETA PRODUCER
    t_eta_producer_worker = threading.Thread(
        name='kafka_eta_producer_worker',
        daemon=True,
        target=kafka_eta_producer_worker,
        args=(eta_mq,)
    )
    threads.append(t_eta_producer_worker)

    # DELIVERY PRODUCER
    t_delivery_producer_worker = threading.Thread(
        name='kafka_delivery_producer_worker',
        daemon=True,
        target=kafka_delivery_producer_worker,
        args=(delivery_mq,)
    )
    threads.append(t_delivery_producer_worker)


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
