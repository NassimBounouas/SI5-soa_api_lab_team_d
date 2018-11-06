#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import subprocess

__product__ = "Uberoo Behaviour Test Suite"
__author__ = "Nikita ROUSSEAU"
__copyright__ = "Copyright 2018, Polytech Nice Sophia"
__credits__ = ["Nikita Rousseau"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Nikita ROUSSEAU"
__email__ = "nikita.rousseau@etu.unice.fr"
__status__ = "development"

if __name__ == '__main__':

    # LOGGING
    logging.basicConfig(
        level=logging.INFO
    )

    # Start
    logging.warning(__product__ + ' version ' + __version__ + ' is starting...')

    # Behave

    result = subprocess.run(['behave'], stdout=subprocess.PIPE)
    logging.info(result.stdout.decode('utf-8'))

    # End

    logging.info('Bye !')
    exit(0)
