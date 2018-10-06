#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.category import Category
from model.persistent_object import PersistentObject


class Meal(PersistentObject):
    identifier = 0
    parent_category = None
    
    name = ""
    price = 0.0
    is_menu = False
    image = ""

    def __init__(self, parent_category: Category, name, price, is_menu=False):
        self.parent_category = parent_category
        self.name = name
        self.price = price

        self.is_menu = is_menu
        self.image = ""

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name,
            "price": self.price,
            "category": self.parent_category.name,
            "is_menu": self.is_menu
        }
