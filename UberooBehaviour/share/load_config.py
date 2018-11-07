#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os
from pathlib import Path


def load_config():
    """
    Parse database configuration file
    """
    config_file = os.path.join(
        Path(os.path.dirname(os.path.realpath(__file__))).parent,
        "config.ini"
    )
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)
    app_config = configparser.ConfigParser()
    app_config.read(config_file)
    return app_config['uberoo']
