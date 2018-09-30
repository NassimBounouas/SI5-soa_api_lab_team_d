#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Category:
    identifier = 0
    name = ""
    region = ""
    image = ""

    def __init__(self, name, region):
        self.name = name
        self.region = region

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name,
            "region": self.region
        }
