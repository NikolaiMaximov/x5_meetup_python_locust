#!/usr/bin/env python
# coding: utf-8

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

import gevent.monkey
gevent.monkey.patch_all()

from log_config import logger
import influx_writer
import time


def check_request(endpoint, request):
    response_body = request.text
    response_status_code = request.status_code

    if 'FIRST' in response_body or 'SECOND' in response_body:
        response_time = int(request.elapsed.total_seconds() * 1000)
        save_influx_stats(
            transaction_name=endpoint,
            response_time=response_time
        )
        logger.write_log(endpoint, ' - ', str(response_time), ' ms', log_type='DEBUG')

    else:
        request.failure('User redirected')
        logger.write_log(endpoint, ' - ', str(response_status_code), ' - response body: ', response_body, log_type='ERROR')


def save_influx_stats(transaction_name=None, response_time=0):
    transaction_end_time = time.time()
    influx_writer.send_response_time(transaction_name,
                                     response_time,
                                     transaction_end_time)
