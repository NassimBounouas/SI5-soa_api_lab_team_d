import configparser
import json
import os
import signal
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


# GLOBAL APPLICATION CONFIGURATION
app_config = []
bootstrap_servers = ()
# GLOBAL THREAD REGISTRY
threads = []

app = Flask(__name__)


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
def hello_world():
    print(g.mq)
    return 'Hello World!'


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

    while True:
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

    # producer.close()
    # return


if __name__ == '__main__':
    # ENVIRONMENT
    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = 'development'
    if 'FLASK_APP' not in os.environ:
        os.environ['FLASK_APP'] = __file__ + '.py'
    env = os.environ['FLASK_ENV']

    # CONFIGURATION
    app_config = __load_config()[env]

    if ',' in str(app_config['bootstrap_servers']):
        bootstrap_servers = list(filter(None, str(app_config['bootstrap_servers']).split(',')))
    else:
        bootstrap_servers = str(app_config['bootstrap_servers'])

    # Logging
    app.logger.removeHandler(default_handler)

    # PRODUCER
    mq = queue.Queue()  # Shared message queue
    g.mq = mq  # Store global

    t_producer_worker = threading.Thread(
        name='kafka_producer_worker',
        daemon=True,
        target=kafka_producer_worker,
        args=('restaurant', mq,)
    )
    threads.append(t_producer_worker)

    # Start
    logging.info('Starting...')
    # Starting threads
    for t in threads:
        t.start()

    logging.info(__product__ + ' version:' + __version__ + ' is now online (`' + env + '` environment')

    # Http server
    app.run("0.0.0.0", port=5000, debug=False)

    # Waiting threads...
    for t in threads:
        t.join()

    logging.info('Bye !')
    exit(0)
