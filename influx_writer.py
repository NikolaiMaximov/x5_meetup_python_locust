#!/usr/bin/env python
# coding: utf-8

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

from influxdb import InfluxDBClient
from datetime import datetime
from config import settings


client = InfluxDBClient(host=settings.INFLUX_DB_HOST, port=settings.INFLUX_DB_PORT)
client.switch_database(settings.INFLUX_DB_DATABASE)


def send_response_time(transaction_name, response_time, timestamp):
    json_body = [
        {
            "measurement": "demo02_response_time",
            "tags": {
                "transaction_name": transaction_name
            },
            "fields": {
                "response_time": response_time
            }
        }
    ]
    client.write_points(json_body)
