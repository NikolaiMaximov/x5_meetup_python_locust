# 17.11.2021 - MeetUp - Нагрузочное тестирование с помощью Python.

1. Locust file -> rest_api_locustfile.py

Чеклист для запуска теста:

1. Требуемые пакеты: pip install locust pydantic influxdb fastapi logging 
2. Установить uvicorn
3. Поднять сервер с заглушкой -> uvicorn locust_mock:app --port 9090 --timeout-keep-alive 120
4. Поднять сервер с Grafana (опционально)
5. Поднять сервер с InfluxDB (порт 8086)
