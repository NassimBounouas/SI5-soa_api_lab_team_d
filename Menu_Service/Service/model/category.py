#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from model.persistent_object import PersistentObject


class Category(PersistentObject):
    identifier = 0

    name = ""
    region = ""
    image = ""

    def __init__(self, dbh=None, pk=0, name="", region="", image=""):
        super().__init__(dbh)

        self.identifier = pk
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
        else:
            # Verify that the record exists
            with self.database_handle.cursor() as cursor:
                sql = "SELECT * FROM category WHERE idcategory=%s"
                cursor.execute(sql, self.identifier)
                if cursor.rowcount != 1:
                    raise ValueError('Bad category identifier !')
                # Complete missing attributes
                row = cursor.fetchone()
                if len(self.name) == 0:
                    self.name = row['name']
                if len(self.region) == 0:
                    self.region = row['region']
                if len(self.image) == 0:
                    self.region = row['image']

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update if required
                sql = "SELECT * FROM category WHERE idcategory=%s"
                cursor.execute(sql, (self.identifier,))
                row = cursor.fetchone()
                # Compute Hash
                b2s = hashlib.blake2s(digest_size=8)
                h = ''
                for attr in row.items():
                    h = h + str(attr[1])
                b2s.update(h.encode('utf-8'))
                fingerprint = b2s.hexdigest()
                if fingerprint != self.hash_id():
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

    def hash_id(self):
        b2s = hashlib.blake2s(digest_size=8)
        h = str(self.identifier) + self.name + self.region + self.image
        b2s.update(h.encode('utf-8'))
        return b2s.hexdigest()

    @staticmethod
    def get_by_name(name, dbh):
        category = Category(dbh=dbh, name=name)
        if category.identifier == 0:
            return None
        return category

    @staticmethod
    def get_by_id(pk, dbh):
        category = Category(dbh=dbh, pk=pk)
        if category.identifier == 0:
            return None
        return category
