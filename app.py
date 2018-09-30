#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, g, jsonify

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


@app.before_request
def before_request():
    """
    Populate Database
    """
    # DB Mock
    g.database = {}
    g.database["categories"] = {}
    g.database["meals"] = {}

    # Categories
    asie_japon = Category("Japonais", "Asie")
    asie_chine = Category("Chinois", "Asie")

    # Meals
    sushis_saumon = Meal(asie_japon, "Sushis saumon", 3.90)
    sushis_saumon_epice = Meal(asie_japon, "Sushis saumon épicé", 4.50)
    sushis_saumon_marine = Meal(asie_japon, "Sushis saumon mariné au jus de yuzu et ses herbes", 4.80)
    brochette_de_viande_fromage = Meal(asie_chine, "Brochette de viande au fromage", 13.90)

    # Meals as Menus
    plateau1_8pcs = Meal(asie_japon, "Plateau 1 - 8 pièces", 13.90, True)

    # Populate
    g.database["categories"][1] = asie_japon
    g.database["categories"][2] = asie_chine

    g.database["meals"][1] = sushis_saumon
    g.database["meals"][2] = sushis_saumon_epice
    g.database["meals"][3] = sushis_saumon_marine
    g.database["meals"][4] = brochette_de_viande_fromage
    g.database["meals"][5] = plateau1_8pcs


@app.route('/')
def hello_world():
    return 'Menu service is online !'


@app.route("/categories",
           methods=['GET'])
def categories_route():

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


@app.route("/meals/<string:category>",
           methods=['GET'])
def meals_route(category: str):

    meals = []

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
