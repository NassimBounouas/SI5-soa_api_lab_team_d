#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kafka import KafkaProducer

"""
# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test',
                         bootstrap_servers=['mint-virtual-machine:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
"""

producer = KafkaProducer(bootstrap_servers='mint-virtual-machine:9092', acks='all')
for _ in range(10):
    producer.send('test', b'some_message_bytes')


producer.flush()
