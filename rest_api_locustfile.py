#!/usr/bin/env python
# coding: utf-8

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

'''Обязательный блок кода, без которого ничего не работает'''
import gevent.monkey
gevent.monkey.patch_all()

'''Импорт библиотеки locust'''
import locust

'''Опциональные импорты. Зависят от ваших потребностей'''
import response_checker
import requests
import os
from config import settings
from log_config import logger


user_id = 0


'''Пользовательский класс, описывающий план теста'''
class DemoUser(locust.HttpUser):
    '''Переменная, в которой мы задаем pacing'''
    wait_time = locust.constant_pacing(settings.TEST_PACING_SEC)

    '''Метод, который выполняется один раз за тест (перед его началом)'''
    @locust.events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        os.remove(settings.LOGGING_FILE)
        logger.write_log('TEST STARTED', log_type='DEBUG')

    '''Метод, который выполняется перед стартом каждого виртуального пользователя'''
    def on_start(self):
        self.login_to_server()

    '''Ряд методов с аннотацией @locust.task реализует бизнес- транзакции, участвующие в нагрузочном тестировании'''
    @locust.task(5)
    def send_first_request(self):
        endpoint = '/action_one'
        self.send_request(endpoint)
        
    @locust.task(3)
    def send_second_request(self):
        endpoint = '/action_two'
        self.send_request(endpoint)   
        
    @locust.task(2)
    def send_third_request(self):
        endpoint = '/action_three'
        self.send_request(endpoint)

    '''Отправка http запросов на сервер'''
    def send_request(self, endpoint):
        url = settings.TESTING_HOST + endpoint
        headers = {
            'accept': 'text/html',
            'accept-encoding' : 'gzip, deflate, br',
            'accept-language' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'token': self.token_id
        }
        with self.client.get(url, headers=headers, catch_response=True) as request:
            response_checker.check_request(endpoint, request)

    '''Метод, который выполняется перед остановкой каждого виртуального пользователя'''
    def on_stop(self):
        logger.write_log('USER ', str(self.user_id), ' STOPPED', log_type='DEBUG')

    '''Метод, который выполняется один раз за тест (перед его остановкой)'''
    @locust.events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        logger.write_log('TEST STOPPED', log_type='DEBUG')

    '''Метод, осуществляющий логин в систему'''
    def login_to_server(self):
        global user_id
        user_id += 1
        self.user_id = user_id
        endpoint = '/login/user' + str(user_id)
        url = settings.TESTING_HOST + endpoint
        request = requests.get(url)
        self.token_id = request.text
        response_time = int(request.elapsed.total_seconds() * 1000)
        locust.events.request.fire(
            request_type='GET',
            name='/login',
            response_time=response_time,
            response_length=0,
            context=None,
            exception=None
        )
        response_checker.save_influx_stats(
            transaction_name='/login',
            response_time=response_time
        )

'''Класс, описывающий алгоритм входа и выхода виртуальных пользователей'''
class StagesShape(locust.LoadTestShape):

    stages = [
        {"duration":20,"users":1,"spawn_rate":1},
        {"duration":40,"users":5,"spawn_rate":1},
        {"duration":60,"users":3,"spawn_rate":1},
        {"duration":80,"users":10,"spawn_rate":1},
        {"duration":100,"users":1,"spawn_rate":1}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None