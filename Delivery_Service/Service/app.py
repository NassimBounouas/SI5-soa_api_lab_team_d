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
    from model.category import Category
    from model.meal import Meal
    from model.restaurant import Restaurant

    dbh = __mysql_connect()

    # Restaurants
    dragon_or = Restaurant(dbh=dbh, name="Dragon d'Or")
    yakuzas = Restaurant(dbh=dbh, name="Le cercle des Yakuzas")

    # Categories
    asie_japon = Category(dbh=dbh, name="Japonais", region="Asie")
    asie_chine = Category(dbh=dbh, name="Chinois", region="Asie")

    # Meals
    Meal(dbh=dbh, parent_restaurant=dragon_or, parent_category=asie_japon, name="Sushis saumon", price=3.90)
    Meal(dbh=dbh, parent_restaurant=dragon_or, parent_category=asie_japon, name="Sushis saumon épicé", price=4.50)
    Meal(dbh=dbh, parent_restaurant=dragon_or, parent_category=asie_japon,
         name="Sushis saumon mariné au jus de yuzu et ses herbes", price=4.80)
    Meal(dbh=dbh, parent_restaurant=dragon_or, parent_category=asie_japon, name="Ramen nature", price=7.0)
    Meal(dbh=dbh, parent_restaurant=yakuzas, parent_category=asie_chine, name="Brochette de viande au fromage",
         price=13.90)

    # Meals as Menus
    Meal(dbh=dbh, parent_restaurant=yakuzas, parent_category=asie_japon, name="Plateau 1 - 8 pièces", price=13.90,
         is_menu=True)

    __mysql_close(dbh)


# BUSINESS FUNCTIONS


def get_categories(dbh, request_id):
    """
    List available categories
    :param dbh: database_handle
    :param request_id: int
    :return: json
    """
    from model.category_collection import CategoryCollection

    categories = CategoryCollection(dbh=dbh)

    return {
        'action': 'CATEGORY_LIST_RESPONSE',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'categories': categories.to_json()
        }
    }


def get_meals_by_category(dbh, request_id, params: dict):
    """
    List food by category
    :param dbh: database_handle
    :param request_id: int
    :param params: dict
    :return: json
    """
    from model.meal_collection import MealCollection

    if not params["category"]:
        return {
            'action': 'FOOD_LIST_RESPONSE',
            'message': {
                'status': 'KO',
                'request': int(request_id),
                'meals': []
            }
        }
    category = params["category"]

    meals = MealCollection(dbh=dbh, category=category)

    return {
        'action': 'FOOD_LIST_RESPONSE',
        'message': {
            'status': 'OK',
            'request': int(request_id),
            'meals': meals.to_json()
        }
    }


# THREAD WORKERS

def kafka_restaurant_producer_worker(mq: queue.Queue):
    """
    Kafka Restaurant Topic Producer
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
                logging.info("GET %s FROM QUEUE AND SENDING TO %s" % (msg, 'restaurant'))
                producer.send('restaurant', msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return


def kafka_restaurant_consumer_worker(mq: queue.Queue):
    """
    Kafka Restaurant Topic Consumer
    as thread worker
    :param mq: queue.Queue
    :return:
    """
    global app_config

    # Client
    consumer = KafkaConsumer('restaurant',
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
                if str(message.value["action"]).upper() == "CATEGORY_LIST_REQUEST":
                    logging.info("PUT get_categories MESSAGE in QUEUE")
                    mq.put(
                        get_categories(
                            dbh,
                            int(message.value["message"]["request"])
                        )
                    )
                elif str(message.value["action"]).upper() == "FOOD_LIST_REQUEST":
                    logging.info("PUT get_meals_by_category MESSAGE in QUEUE")
                    mq.put(
                        get_meals_by_category(
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

    consumer.close()
    return


# MAIN

if __name__ == "__main__":
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'production':
        env = 'production'

    # LOGGING
    if env == 'production':
        logging.basicConfig(
            level=logging.WARNING
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

    # RESTAURANT CONSUMER
    restaurant_mq = queue.Queue()  # Shared queue between consumer / producer threads

    t_kafka_restaurant_consumer_worker = threading.Thread(
        name='kafka_consumer_worker',
        daemon=True,
        target=kafka_restaurant_consumer_worker,
        args=(restaurant_mq,)
    )
    threads.append(t_kafka_restaurant_consumer_worker)

    # PRODUCER
    t_producer_worker = threading.Thread(
        name='kafka_producer_worker',
        daemon=True,
        target=kafka_restaurant_producer_worker,
        args=(restaurant_mq,)
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
