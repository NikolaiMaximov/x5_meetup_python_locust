# -*- coding: utf-8 -*-

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

import pydantic


class Settings(pydantic.BaseSettings):      
    TEST_PACING_SEC: int = 5
 
    INFLUX_DB_HOST: str = 'localhost'
    INFLUX_DB_PORT: int = 8086
    INFLUX_DB_DATABASE: str = "presentation_demo"

    LOGGING_FILE: str = 'logs.log'
    LOGGING_ENCODING: str = 'utf-8'
    LOGGING_LOGGER_NAME: str = 'demo_logger'
    LOGGING_FORMAT: str = '%(asctime)s %(levelname)s: %(message)s'
    LOGGING_LEVEL: str = 'DEBUG'
    
    PROTOCOL: str = 'http'
    HOST_NAME: str = 'localhost'
    PORT: str = '9090'
    HOST_TUPLE: tuple = (PROTOCOL, '://', HOST_NAME, ':', PORT)
    TESTING_HOST: str = ''.join(HOST_TUPLE)


settings = Settings()