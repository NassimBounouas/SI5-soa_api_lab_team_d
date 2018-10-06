#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import json
import os
import pymysql.cursors

from flask import Flask, g, jsonify, request

from model.category import Category
from model.category_collection import CategoryCollection
from model.meal import Meal
from model.meal_collection import MealCollection

__product__ = "Menu Service"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nikita Rousseau"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"

app = Flask(__name__)


def load_config():
    """
    Parse database configuration file
    """
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.ini")
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config


def __populate_db():
    """
    DATABASE IMPORT
    """
    # Categories
    asie_japon = Category(name="Japonais", region="Asie")
    asie_chine = Category(name="Chinois", region="Asie")

    # Meals
    Meal(asie_japon, "Sushis saumon", 3.90)
    Meal(asie_japon, "Sushis saumon épicé", 4.50)
    Meal(asie_japon, "Sushis saumon mariné au jus de yuzu et ses herbes", 4.80)
    Meal(asie_japon, "Ramen nature", 7.0)
    Meal(asie_chine, "Brochette de viande au fromage", 13.90)

    # Meals as Menus
    Meal(asie_japon, "Plateau 1 - 8 pièces", 13.90, True)

    # Mark as ready
    g.database_is_ready = True


@app.before_request
def before_request():
    # DATABASE CONNECTION
    g.database_handle = None

    # LOAD CONFIGURATION
    if not os.environ['FLASK_ENV']:
        os.environ['FLASK_ENV'] = 'development'

    db_config = load_config()[os.environ['FLASK_ENV']]

    # Connect to the database
    g.database_handle = pymysql.connect(host=db_config['host'],
                                        port=int(db_config['port']),
                                        user=db_config['user'],
                                        password=db_config['pass'],
                                        db=db_config['db'],
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor,
                                        autocommit=True)

    if not hasattr(g, 'database_is_ready'):
        __populate_db()


@app.after_request
def after_request(response):
    # DISCONNECT FROM THE DATABASE
    g.database_handle.close()
    return response


@app.route('/')
def hello_world():
    return 'Menu service is online !'


@app.route("/receive_event",
           methods=['POST'])
def event_listener_route():
    event = json.loads(request.data.decode('utf-8'))

    if event["Action"] == 'READ_CATEGORIES':
        return getCategories()

    if event["Action"] == 'READ_MEALS_BY_CATEGORY':
        return getMealsByCategory(event["Message"])

    return jsonify(""), 400


def getCategories():
    categories = CategoryCollection()

    data = {
        'status': 'OK',
        'categories': categories.to_json()
    }

    return jsonify(data), 200


def getMealsByCategory(params: dict):
    if not params["Category"]:
        jsonify([]), 400
    category = params["Category"]

    meals = MealCollection(category)

    data = {
        'status': 'OK',
        'meals': meals.to_json()
    }

    return jsonify(data), 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=False)
