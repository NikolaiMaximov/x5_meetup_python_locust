#!/usr/bin/env python
# coding: utf-8

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

import logging
from config import settings


class LogConfig():

    logger = logging.getLogger(settings.LOGGING_LOGGER_NAME)
    logger.setLevel(settings.LOGGING_LEVEL)
    file = logging.FileHandler(filename=settings.LOGGING_FILE)
    file.setFormatter(logging.Formatter(settings.LOGGING_FORMAT))
    logger.addHandler(file)
    logger.propagate = False  # Disables console output

    def write_log(self, *args, log_type):
        log_string = args
        if log_type == 'ERROR':
            self.logger.error(''.join(log_string))
        if log_type == 'DEBUG':
            self.logger.debug(''.join(log_string))


logger = LogConfig()
