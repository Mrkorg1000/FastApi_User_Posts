# Тестовое задание. Компания "Webtronics"

Простое RESTful API с использованием FastAPI для условного приложения типа социальных сетей.

# Стек

* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker/Docker-compose


# Инструкция по локальному запуску/тестированию проекта


`docker-compose up -d` -- поднимаем Базу Данных и Adminer для работы с БД в контейнерах.

`uvicorn main:app --reload` -- запуск приложения

`API_DEBUG` -- если установлена в `true`, то при перезапуске АПИ будет стираться содержимое БД
