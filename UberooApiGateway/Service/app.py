import configparser
import json
import os
import signal
import sys
import threading
import queue
import logging

from flask.logging import default_handler
from kafka import KafkaProducer
from kafka import KafkaConsumer
from flask import Flask, g, jsonify, request

__product__ = "Uberoo Api Gateay"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nikita Rousseau"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"


# Flask Application
app = Flask(__name__)


# GLOBAL APPLICATION CONFIGURATION
app_config = []
bootstrap_servers = ()
topics = ()
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


signal.signal(signal.SIGINT, __sigint_handler)
signal.signal(signal.SIGTERM, __sigint_handler)


def __load_config():
    """
    Parse database configuration file
    """
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config


@app.route('/')
def root_route():
    global mq

    mq.put('TOTO')

    return 'Hello World!'


@app.route('/status')
def status_route():
    return jsonify(''), 200


def http_server_worker():
    # Http server
    app.run("0.0.0.0", port=5000, use_reloader=False, threaded=True)
    return


def kafka_producer_worker(topic: str, mq: queue.Queue):
    """
    Kafka Generic Message Producer
    as thread worker
    Get messages from a shared mq queue.Queue
    :param topic: str
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
                logging.info("GET %s FROM QUEUE AND SENDING TO %s" % (msg, topic))
                producer.send(topic, msg)
                # Force buffer flush in order to send the message
                logging.info("MESSAGE SENT !")
                producer.flush()
        except Exception as e:
            logging.fatal(e, exc_info=True)

    producer.close()
    return


if __name__ == '__main__':
    # ENVIRONMENT

    env = 'development'
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'production':
        env = 'production'

    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = env
    if 'FLASK_APP' not in os.environ:
        os.environ['FLASK_APP'] = __file__ + '.py'

    if env == 'development':
        os.environ['FLASK_DEBUG'] = '1'
    else:
        os.environ['FLASK_DEBUG'] = '0'

    # LOGGING
    app.logger.removeHandler(default_handler)
    if env == 'production':
        logging.basicConfig(
            level=logging.WARNING
        )
    else:
        logging.basicConfig(
            level=logging.INFO
        )

    # CONFIGURATION
    app_config = __load_config()[env]

    # Bootstrap servers
    if ',' in str(app_config['bootstrap_servers']):
        bootstrap_servers = list(filter(None, str(app_config['bootstrap_servers']).split(',')))
    else:
        bootstrap_servers = str(app_config['bootstrap_servers'])

    # Topics
    if ',' in str(app_config['topics']):
        topics = list(filter(None, str(app_config['topics']).split(',')))
    else:
        topics = str(app_config['topics'])

    # WERKZEUG SERVER
    t_http_server_worker = threading.Thread(
        name='http_server_worker',
        daemon=True,
        target=http_server_worker
    )

    ###########################################################

    # PRODUCER
    mq = queue.Queue()  # Shared message queue

    t_producer_worker = threading.Thread(
        name='kafka_producer_worker',
        daemon=True,
        target=kafka_producer_worker,
        args=('restaurant', mq,)
    )
    threads.append(t_producer_worker)

    ###########################################################

    # Start
    logging.warning(__product__ + ' version ' + __version__ + ' (' + env + ') is starting...')
    logging.warning('It may take up to 60 seconds before running !')

    # Starting threads
    for t in threads:
        t.start()
    t_http_server_worker.start()

    # Waiting threads...
    for t in threads:
        t.join()
    t_http_server_worker.join()

    logging.info('Bye !')
    exit(0)
