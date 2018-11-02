#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from model.persistent_object import PersistentObject


class Restaurant(PersistentObject):
    identifier = 0

    name = ""

    def __init__(self, dbh=None, pk=0, name=""):
        super().__init__(dbh)

        self.identifier = pk
        self.name = name

        # Sync
        self.merge()

    def __resolve_identifier(self):
        if self.identifier < 1:
            with self.database_handle.cursor() as cursor:
                sql = "SELECT idrestaurant FROM restaurant WHERE name=%s"
                cursor.execute(sql, self.name)
                if cursor.rowcount > 0:
                    self.identifier = cursor.fetchone()["idrestaurant"]
        else:
            # Verify that the record exists
            with self.database_handle.cursor() as cursor:
                sql = "SELECT * FROM restaurant WHERE idrestaurant=%s"
                cursor.execute(sql, self.identifier)
                if cursor.rowcount != 1:
                    raise ValueError('Bad restaurant identifier !')
                # Complete missing attributes
                row = cursor.fetchone()
                if len(self.name) == 0:
                    self.name = row['name']

    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update if required
                sql = "SELECT * FROM restaurant WHERE idrestaurant=%s"
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
                    sql = "UPDATE restaurant SET name=%s WHERE idrestaurant=%s"
                    cursor.execute(sql, (self.name, self.identifier))
            else:
                # Create
                sql = "INSERT INTO restaurant (name) VALUES (%s)"
                cursor.execute(sql, (self.name,))
                # Fetch identifier
                self.identifier = cursor.lastrowid

    def delete(self):
        self.__resolve_identifier()

        if self.identifier < 1:
            return

        with self.database_handle.cursor() as cursor:
            sql = "DELETE FROM restaurant WHERE idrestaurant=%s"
            cursor.execute(sql, self.identifier)
            self.identifier = 0

    def to_json(self):
        return {
            "id": self.identifier,
            "name": self.name
        }

    def hash_id(self):
        b2s = hashlib.blake2s(digest_size=8)
        h = str(self.identifier) + self.name
        b2s.update(h.encode('utf-8'))
        return b2s.hexdigest()

    @staticmethod
    def get_by_name(name, dbh):
        restaurant = Restaurant(dbh=dbh, name=name)
        if restaurant.identifier == 0:
            return None
        return restaurant

    @staticmethod
    def get_by_id(pk, dbh):
        restaurant = Restaurant(dbh=dbh, pk=pk)
        if restaurant.identifier == 0:
            return None
        return restaurant
