#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PersistentObject:
    database_handle = None

    def __init__(self, dbh):
        self.database_handle = dbh

    def merge(self):
        pass

    def delete(self):
        pass
