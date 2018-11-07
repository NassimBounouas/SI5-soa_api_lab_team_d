#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import subprocess

from share.load_config import load_config

__product__ = "Uberoo Behaviour Test Suite"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nikita Rousseau"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"

# APP CONFIG
behave_config = {}

# API GATEWAY ENDPOINT
endpoint = ''


if __name__ == '__main__':

    # LOGGING
    logging.basicConfig(
        level=logging.INFO
    )

    # CONFIGURATION
    behave_config = load_config()
    endpoint = behave_config['api_gateway_endpoint']

    # Start
    logging.warning(__product__ + ' version ' + __version__ + ' is starting...')
    logging.warning('Api-gateway endpoint : ' + endpoint)

    # Behave

    result = subprocess.run(['behave'], stdout=subprocess.PIPE)
    logging.info(result.stdout.decode('utf-8'))

    # End

    logging.info('Bye !')
    exit(0)
