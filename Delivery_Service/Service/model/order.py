#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from model.persistent_object import PersistentObject

class Order(PersistentObject):
    identifier = 0

    meal_name = None
    pickup_restaurant = None
    pickup_date = None
    delivery_address = ""

    def __init__(self, dbh=None, pk=0, meal_name=None, pickup_restaurant=None, pickup_date=None, delivery_address=None):
        super().__init__(dbh)

        if meal_name is None:
            raise ValueError('An order must be bound to an order!')
        if pickup_restaurant is None:
            raise ValueError('An order must be bound to a restaurant !')
        if pickup_date is None:
            raise ValueError('An order must be bound to a pickup date !')
        if delivery_address is None:
            raise ValueError('An order must be bound to a delivery address !')
        self.identifier = pk

        self.meal_name = meal_name
        self.pickup_restaurant = pickup_restaurant
        self.pickup_date = pickup_date
        self.delivery_address = delivery_address
        self.status = "WAITING"
        self.id_steed = 1
        # Sync
        self.merge()

    def __resolve_identifier(self):
        if self.identifier < 1:
            with self.database_handle.cursor() as cursor:
                sql = "SELECT id FROM to_deliver_table WHERE meal_name=%s AND pickup_restaurant=%s AND pickup_date=%s AND delivery_address=%s"
                data = (self.meal_name, self.pickup_restaurant, self.pickup_date, self.delivery_address)
                cursor.execute(sql, data)
                if cursor.rowcount > 0:
                    self.identifier = cursor.fetchone()["id"]
        else:
            # Verify that the record exists
            with self.database_handle.cursor() as cursor:
                sql = "SELECT * FROM to_deliver_table WHERE id=%s"
                cursor.execute(sql, self.identifier)
                if cursor.rowcount != 1:
                    raise ValueError('Bad order identifier !')
                # Complete missing attributes
                row = cursor.fetchone()
                if len(self.meal_name) == 0:
                    self.meal_name = row['meal_name']
                if len(self.pickup_restaurant) == 0:
                    self.pickup_restaurant = row['pickup_restaurant']
                if self.pickup_date is None:
                    self.pickup_date = row['pickup_date']
                if len(self.delivery_address) == 0:
                    self.delivery_address = row['delivery_address']
                if len(self.status) == 0:
                    self.status = row['status']
                if self.id_steed is None:
                    self.id_steed = row['id_steed']


    def merge(self):
        self.__resolve_identifier()

        # Update fields
        with self.database_handle.cursor() as cursor:
            if self.identifier > 0:
                # Update if required
                sql = "SELECT * FROM to_deliver_table WHERE id=%s"
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
                    sql = "UPDATE to_deliver_table SET meal_name=%s, pickup_restaurant=%s, pickup_date=%s, delivery_address=%s, status=%s, id_steed=%s WHERE id=%s"
                    cursor.execute(sql, (self.meal_name, self.pickup_restaurant, self.pickup_date, self.delivery_address, self.status, self.id_steed, self.identifier))
            else:
                # Create
                sql = "INSERT INTO to_deliver_table (id, meal_name, pickup_restaurant, pickup_date, delivery_address, status, id_steed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (self.identifier, self.meal_name, self.pickup_restaurant, self.pickup_date, self.delivery_address, self.status, self.id_steed))
                # Fetch identifier
                self.identifier = cursor.lastrowid

    def delete(self):
        self.__resolve_identifier()

        if self.identifier < 1:
            return

        with self.database_handle.cursor() as cursor:
            sql = "DELETE FROM to_deliver_table WHERE id=%s"
            cursor.execute(sql, self.identifier)
            self.identifier = 0

    def to_json(self):
        return {
            "id": self.identifier,
            "meal_name": self.meal_name,
            "pickup_restaurant": self.pickup_restaurant,
            "pickup_date": self.pickup_date,
            "delivery_address": self.delivery_address,
            "status": self.status,
            "id_steed": self.id_steed
        }

    def hash_id(self):
        b2s = hashlib.blake2s(digest_size=8)
        h = str(self.identifier) + self.meal_name + self.pickup_restaurant + str(self.pickup_date) + self.delivery_address + self.status
        b2s.update(h.encode('utf-8'))
        return b2s.hexdigest()