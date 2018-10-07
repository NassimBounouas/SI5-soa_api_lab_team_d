#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.persistent_object import PersistentObject


class Category(PersistentObject):
    identifier = 0

    name = ""
    region = ""
    image = ""

    def __init__(self, name="", region="", image=""):
        PersistentObject.__init__(self)

        self.name = name
        self.region = region
        self.image = image

        # Sync
        self.merge()

    def __resolve_identifier(self):
        if self.identifier < 1:
            with self.database_handle.cursor() as cursor:
                sql = "SELECT idcategory FROM category WHERE name=%s"
                cursor.execute(sql, self.name)
                if cursor.rowcount > 0:
                    self.identifier = cursor.fetchone()["idcategory"]

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update
                sql = "UPDATE category SET name=%s, region=%s, image=%s WHERE idcategory=%s"
                cursor.execute(sql, (self.name, self.region, self.image, self.identifier))
            else:
                # Create
                sql = "INSERT INTO category (name, region, image) VALUES (%s, %s, %s)"
                cursor.execute(sql, (self.name, self.region, self.image))
                # Fetch identifier
                self.identifier = cursor.lastrowid

    def delete(self):
        self.__resolve_identifier()

        if self.identifier < 1:
            return

        with self.database_handle.cursor() as cursor:
            sql = "DELETE FROM category WHERE idcategory=%s"
            cursor.execute(sql, self.identifier)
            self.identifier = 0

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name,
            "region": self.region
        }

    @staticmethod
    def get_by_name(name):
        category = Category(name=name)
        if category.identifier == 0:
            return None
        return category
