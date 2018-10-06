#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g


class PersistentObject:
    database_handle = None

    def __init__(self):
        self.database_handle = g.database_handle
