# Запуск

## На windows:

1. Выпустить сертификаты для ssh `mkcert localhost 127.0.0.1 ::1`
2. Переименовать ключ в `key.pem`
3. Переименовать сертификат в `cert.pem`
4. Выполнить `poetry install`
5. Выполнить `uvicorn src.lti_auth.app:app --reload --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem`

## На linux / mac os



## В Docker

to be later


# Переменные окружения

См. `src.settings.settings.py` - создается объект настроек из `.env` файла

Там заданы дефолтные значения + дано краткое описание, за что именно отвечает та или иная настройка


# Реализованные обработчики

## Обработчик запроса инициализации от moodle


| Название       | Характеристика                                                    |
|----------------|-------------------------------------------------------------------|
| url            | `/public/v1/lti/`                                                 |
| Формат запроса | form data                                                         |
| Схема запроса  | см стандарт ([ссылка](https://devhub.educacional.com/docs/lti1o)) |


## Обработчик отправки результата проверки в moodle
| Название       | Характеристика                                                                                                                                                                                                                                                                                                                                                                            |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| url            | `/public/v1/send-mark/`                                                                                                                                                                                                                                                                                                                                                                   |
| Формат запроса | json                                                                                                                                                                                                                                                                                                                                                                                      |
| Схема запроса  | <pre>{<br>  "$schema": "http://json-schema.org/draft-04/schema#",<br>  "type": "object",<br>  "properties": {<br>    "mark": {<br>      "type": "integer"<br>    },<br>    "lti_user_id": {<br>      "type": "string"<br>    },<br>    "task_id": {<br>      "type": "string"<br>    }<br>  },<br>  "required": [<br>    "mark",<br>    "lti_user_id",<br>    "task_id"<br>  ]<br>}</pre> |


## Обработчик получения данных о пользователе для приложения-исполнителя
| Название       | Характеристика              |
|----------------|-----------------------------|
| url            | `/public/v1/get-user-info/` |
| Формат запроса | json                        |
| Схема запроса  |                             |


# Разработка

## Линтеры и статические анализаторы кода

### Одиночные запуски
1. `python -m ruff check --select I --select T20 --select COM  --select B --exclude B008 --select F --select E --select W --select N --select C90  --fix src`
2. `python -m ruff format src`
3. `python -m mypy --install-types --non-interactive --show-error-context --show-column-numbers --pretty src`
4. `python -m deptry src` - игнорим `python-multipart`, он нужен для `fastapi`
