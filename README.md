# Telegram Booking Bot

Бот для записи клиентов к мастеру (маникюр, брови, ресницы).

## Установка

1. Клонируй репозиторий
2. Создай виртуальное окружение: `python3.12 -m venv venv`
3. Активируй: `source venv/bin/activate`
4. Установи зависимости: `pip install -r requirements.txt`
5. Скопируй `.env.example` в `.env` и заполни значения
6. Запусти БД: `docker-compose up -d`

## Запуск

````bash
python -m app.main

Стек

- Python 3.12+
- aiogram 3
- PostgreSQL
- SQLAlchemy 2 (async)
- APScheduler

## Проверка: Как понять, что этап пройден?

Выполни в терминале:

```bash

ls -la

Ты должен увидеть:

- ✅ Папку app/ с подпапками
- ✅ Файл requirements.txt
- ✅ Файл .env
- ✅ Файл .env.example
- ✅ Файл .gitignore
- ✅ Файл docker-compose.yml
- ✅ Папку venv/

Проверь, что БД запущена:

docker ps

Ты должен увидеть контейнер booking_db.
````

---

## Возможные ошибки

#### 1. `python3.12: command not found`

Решение: Установи Python 3.12 или используй доступную версию (не ниже 3.11)

#### 2. `docker: command not found`

`Решение:` Установи Docker Desktop

#### 3. `Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use`

`Решение:` Порт 5432 занят. Либо останови локальный PostgreSQL, либо измени порт в docker-compose.yml на
5433:5432

#### 4. `pip: command not found`

`Решение:` Используй python -m pip вместо pip
