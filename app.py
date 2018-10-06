#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import json
import os
import pymysql.cursors

from flask import Flask, g, jsonify, request

from model.category import Category
from model.meal import Meal

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


def populate_db():
    """
    DATABASE IMPORT
    """

    # DB Mock
    g.registry = {}
    g.registry["categories"] = {}
    g.registry["meals"] = {}

    # Categories
    asie_japon = Category(name="Japonais", region="Asie")
    asie_chine = Category(name="Chinois", region="Asie")

    # Meals
    sushis_saumon = Meal(asie_japon, "Sushis saumon", 3.90)
    sushis_saumon_epice = Meal(asie_japon, "Sushis saumon épicé", 4.50)
    sushis_saumon_marine = Meal(asie_japon, "Sushis saumon mariné au jus de yuzu et ses herbes", 4.80)
    ramen_nature = Meal(asie_japon, "Ramen nature", 7.0)
    brochette_de_viande_fromage = Meal(asie_chine, "Brochette de viande au fromage", 13.90)

    # Meals as Menus
    plateau1_8pcs = Meal(asie_japon, "Plateau 1 - 8 pièces", 13.90, True)

    # Populate
    g.registry["categories"][1] = asie_japon
    g.registry["categories"][2] = asie_chine

    g.registry["meals"][1] = sushis_saumon
    g.registry["meals"][2] = sushis_saumon_epice
    g.registry["meals"][3] = sushis_saumon_marine
    g.registry["meals"][4] = brochette_de_viande_fromage
    g.registry["meals"][5] = plateau1_8pcs
    g.registry["meals"][6] = ramen_nature


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
                                        cursorclass=pymysql.cursors.DictCursor,
                                        autocommit=True)


@app.after_request
def after_request():
    # DISCONNECT FROM THE DATABASE
    g.database_handle.close()


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
    categories = []

    for identifier in g.database["categories"]:
        category = g.database["categories"][identifier]

        category.identifier = identifier
        categories.append(category.to_json())

    data = {
        'status': 'OK',
        'categories': categories
    }

    return jsonify(data), 200


def getMealsByCategory(params: dict):
    meals = []

    if not params["Category"]:
        jsonify(meals), 400
    category = params["Category"]

    for identifier in g.database["meals"]:
        meal = g.database["meals"][identifier]

        if meal.parent_category.name == category:
            meal.identifier = identifier
            meals.append(meal.to_json())

    data = {
        'status': 'OK',
        'meals': meals
    }

    return jsonify(data), 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=False)
