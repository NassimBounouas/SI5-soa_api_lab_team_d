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
from time import sleep
from flask.logging import default_handler
from kafka import KafkaProducer
from kafka import KafkaConsumer
from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest, NotFound
from message.factory import make_kafka_message

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
env = 'development'
app_config = {}
bootstrap_servers = []
topics = []
messages = {}
# GLOBAL THREAD REGISTRY
threads = []
threads_mq = {}
# CLEAN EXIT EVENT
t_stop_event = threading.Event()

# CALLBACK REGISTRY
# TODO : periodic clean-up of the old callbacks
callback_registry = {}


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
    sys.exit(1)


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


########################################################################################################################
# API GATEWAY ROUTES
########################################################################################################################


@app.route('/')
def root_route():
    # API DOCUMENTATION ROOT
    return render_template('swagger/index.html')


@app.route('/status')
def status_route():
    return jsonify(
        {'status': 'online'}
    ), 200


########################################################################################################################
# MENU SERVICE
########################################################################################################################

@app.route("/list_categories",
           methods=['GET', 'POST'])
def list_categories_route():
    if request.method == 'POST':
        # Build message
        message, request_id = make_kafka_message(
            action='CATEGORY_LIST_REQUEST',
            message={}
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/list_meals_by_category",
           methods=['GET', 'POST'])
def list_meals_by_category_route():
    if request.method == 'POST':
        # Verify user input
        if 'category' not in request.form:
            BadRequest()  # 400

        # Extract params
        category = request.form['category']

        # Build message
        message, request_id = make_kafka_message(
            action='FOOD_LIST_REQUEST',
            message={
                "category": category
            }
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/restaurants",
           methods=['GET', 'POST'])
def list_restaurants_route():
    if request.method == 'POST':

        # Build message
        message, request_id = make_kafka_message(
            action='RESTAURANT_LIST_REQUEST',
            message={}
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/restaurant-menu",
           methods=['GET', 'POST'])
def list_restaurant_menu_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_restaurant' not in request.form:
            BadRequest()  # 400

        # Extract params
        restaurant = request.form['id_restaurant']

        # Build message
        message, request_id = make_kafka_message(
            action='FOOD_MENU_REQUEST',
            message={
                "restaurant": restaurant
            }
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/meal_feedback",
           methods=['POST'])
def meal_feedback_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_meal' not in request.form or 'id_restaurant' not in request.form or 'comment' not in request.form:
            BadRequest()  # 400

        # Extract params
        meal = request.form['id_meal']
        restaurant = request.form['id_restaurant']
        comment = request.form['comment']

        # Build message
        message, request_id = make_kafka_message(
            action='FEEDBACK_REQUEST',
            message={
                "meal": meal,
                "restaurant": restaurant,
                "comment": comment
            }
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202


@app.route("/create_promotional_code",
           methods=['POST'])
def create_promotional_route():
    if request.method == 'POST':
        # Verify user input
        if 'code' not in request.form or 'reduction' not in request.form:
            BadRequest()  # 400

        # Extract params
        code = request.form['code']
        reduction = request.form['reduction']

        # Build message
        message, request_id = make_kafka_message(
            action='CREATE_CODE_REQUEST',
            message={
                "code": code,
                "reduction": reduction
            }
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "Promotional code created"
        }), 200



########################################################################################################################
# ORDERING SERVICE
########################################################################################################################


@app.route("/order",
           methods=['POST'])
def order_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_restaurant' not in request.form or\
                'id_meal' not in request.form or\
                'client_name' not in request.form or\
                'client_address' not in request.form:
            BadRequest()  # 400

        # Extract params
        restaurant = request.form['id_restaurant']
        meal = request.form['id_meal']
        client_name = request.form['client_name']
        client_address = request.form['client_address']

        # Build message
        message, request_id = make_kafka_message(
            action='RESTAURANT_ORDER_REQUEST',
            message={
                "restaurant": restaurant,
                "meal": meal,
                "client_name": client_name,
                "client_address": client_address
            }
        )

        # Send
        threads_mq['ordering'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202


@app.route("/validate-order",
           methods=['POST'])
def validate_order_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_order' not in request.form:
            BadRequest()  # 400

        # Extract params
        order = request.form['id_order']

        # Build message
        message, request_id = make_kafka_message(
            action='VALIDATE_ORDER_REQUEST',
            message={
                "order": order,
            }
        )

        # Send
        threads_mq['ordering'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202


@app.route("/order-status",
           methods=['GET'])
def order_status_route():
    if request.method == 'GET':
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/order_list_by_restaurant",
           methods=['GET', 'POST'])
def order_list_by_restaurant_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_restaurant' not in request.form:
            BadRequest()  # 400

        # Extract params
        restaurant = request.form['id_restaurant']

        # Build message
        message, request_id = make_kafka_message(
            action='ORDER_LIST_REQUEST',
            message={
                "restaurant": restaurant
            }
        )

        # Send
        threads_mq['restaurant'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200

########################################################################################################################
# ETA SERVICE
########################################################################################################################


@app.route("/eta",
           methods=['GET', 'POST'])
def eta_route():
    if request.method == 'POST':
        # Verify user input
        if 'from' not in request.form or 'to' not in request.form:
            BadRequest()  # 400

        # Extract params
        _from = request.form['from']
        _to = request.form['to']

        # Build message
        message, request_id = make_kafka_message(
            action='ETA_REQUEST',
            message={
                "from": _from,
                "to": _to,
            }
        )

        # Send
        threads_mq['eta'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


########################################################################################################################
# PAYWALL SERVICE
########################################################################################################################


@app.route("/paywall",
           methods=['GET', 'POST'])
def pay_order_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_order' not in request.form or 'card_number' not in request.form:
            BadRequest()  # 400

        # Extract params
        order = request.form['id_order']
        card_number = request.form['card_number']

        # Build message
        message, request_id = make_kafka_message(
            action='PAYMENT_PLACED',
            message={
                "order": order,
                "card_number": card_number
            }
        )

        # Send
        threads_mq['ordering'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


########################################################################################################################
# DELIVERY SERVICE
########################################################################################################################


@app.route("/map",
           methods=['GET', 'POST'])
def map_route():
    if request.method == 'POST':
        # Verify user input
        if 'long' not in request.form or 'lat' not in request.form:
            BadRequest()  # 400

        # Extract params
        long = request.form['long']
        lat = request.form['lat']

        # Build message
        message, request_id = make_kafka_message(
            action='MAP_DELIVERY_PROBE',
            message={
                "long": long,
                "lat": lat
            }
        )

        # Send
        threads_mq['delivery'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/notify_delivery",
           methods=['GET', 'POST'])
def notify_delivery_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_order' not in request.form:
            BadRequest()  # 400

        # Extract params
        order = request.form['id_order']

        # Build message
        message, request_id = make_kafka_message(
            action='NOTIFY_DELIVERY_REQUEST',
            message={
                "order": order
            }
        )

        # Send
        threads_mq['delivery'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/delivery_location",
           methods=['GET', 'POST'])
def delivery_location_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_order' not in request.form or 'id_steed' not in request.form or 'lat' not in request.form or 'long' not in request.form:
            BadRequest()  # 400

        # Extract params
        order = request.form['id_order']
        steed = request.form['id_steed']
        lat = request.form['lat']
        long = request.form['long']

        # Build message
        message, request_id = make_kafka_message(
            action='DELIVERY_LOCATION_PUSH',
            message={
                "order": order,
                "steed": steed,
                "lat": lat,
                "long": long
            }
        )

        # Send
        threads_mq['delivery'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        # Response callback
        if 'order' not in request.args:
            raise BadRequest()

        order_id = int(request.args.get("order"))

        # Response
        return jsonify(
            "Your order will arrive in : X minutes"  # TODO: Implement a system to retrieve last position
        ), 200


@app.route("/stats",
           methods=['GET', 'POST'])
def steed_stats_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_steed' not in request.form:
            BadRequest()  # 400

        # Extract params
        steed = request.form['id_steed']

        # Build message
        message, request_id = make_kafka_message(
            action='STEED_STAT_REQUEST',
            message={
                "steed": steed
            }
        )

        # Send
        threads_mq['delivery'].put(message)

        # Response with callback url
        return jsonify({
            "callbackUrl": request.url + '?id=' + str(request_id)
        }), 202
    else:
        if 'id' not in request.args:
            raise BadRequest()

        request_id = int(request.args.get("id"))

        if request_id not in callback_registry:
            raise NotFound()

        # Response
        return jsonify(
            callback_registry[request_id]
        ), 200


@app.route("/steed_status",
           methods=['POST'])
def steed_status_route():
    if request.method == 'POST':
        # Verify user input
        if 'id_steed' not in request.form:
            BadRequest()  # 400

        # Extract params
        steed = request.form['id_steed']
        status = request.form['status']

        # Build message
        message, request_id = make_kafka_message(
            action='SEND_STEED_STATUS',
            message={
                "steed": steed,
                "status": status
            }
        )

        # Send
        threads_mq['delivery'].put(message)

        # Response with callback url
        return jsonify({
            "Status updated"
        }), 200

########################################################################################################################
# END: ROUTES
########################################################################################################################


def http_server_worker():
    # Http server
    app.run("0.0.0.0", port=5000, use_reloader=False, threaded=True)
    return


def kafka_consumer_worker(topic: str, action_whitelist: list):
    """
    Kafka Generic Message Consumer
    as thread worker
    :param topic: str
    :param action_whitelist: list
    :return:
    """
    # Client
    consumer = KafkaConsumer(topic,
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

                request_id = int(message.value["message"]["request"])

                # Action switch
                if str(message.value["action"]).upper() in action_whitelist:
                    logging.info("RESPONSE " + str(request_id) + " (" + str(message.value["action"]).upper() + ")")
                    if request_id not in callback_registry:
                        callback_registry[request_id] = message.value["message"]
        except Exception as e:
            logging.fatal(e, exc_info=True)

    consumer.close()
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


if __name__ == '__main__':
    # ENVIRONMENT
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
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            level=logging.INFO
        )

    # CONFIGURATION
    app_config_raw = __load_config()
    app_config = app_config_raw[env]
    messages = app_config_raw['messages']

    # Bootstrap servers
    if ',' in str(app_config['bootstrap_servers']):
        bootstrap_servers = list(filter(None, str(app_config['bootstrap_servers']).split(',')))
    else:
        bootstrap_servers.append(str(app_config['bootstrap_servers']))

    # Topics
    if ',' in str(app_config['topics']):
        topics = list(filter(None, str(app_config['topics']).split(',')))
    else:
        topics.append(str(app_config['topics']))

    # WERKZEUG SERVER
    t_http_server_worker = threading.Thread(
        name='http_server_worker',
        daemon=True,
        target=http_server_worker
    )

    ###########################################################

    for topic in topics:
        # I/O message queue
        mq = queue.Queue()
        threads_mq[topic] = mq

        # Messages action whitelist
        action_whitelist = []
        if topic in messages:
            if ',' in str(messages[topic]):
                action_whitelist = list(filter(None, str(messages[topic]).split(',')))
            else:
                action_whitelist.append(str(messages[topic]))

        # Producer Worker
        t_producer_worker = threading.Thread(
            name='kafka_' + topic + '_producer_worker',
            daemon=True,
            target=kafka_producer_worker,
            args=(topic, mq,)
        )
        threads.append(t_producer_worker)

        # Consumer Worker
        t_consumer_worker = threading.Thread(
            name='kafka_' + topic + '_consumer_worker',
            daemon=True,
            target=kafka_consumer_worker,
            args=(topic, action_whitelist,)
        )
        threads.append(t_consumer_worker)

    ###########################################################

    # Start
    logging.warning(__product__ + ' version ' + __version__ + ' (' + env + ') is starting...')

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
