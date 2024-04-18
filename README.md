# Запуск

## На linux / mac os / windows

Уточнения:
- На ubuntu22.04 у меня не завелось. Советую использовать 20.04 
- Приведенные команды необходимо выполнять из корня проекта
- При внесении изменений в код, необходимо ребилдить images `docker-compose build`

Порядок действий:
1. Установить `mkcert`, `docker`, `docker-compose`
2. Выпустить сертификаты для ssh `mkcert -key-file key.pem -cert-file cert.pem localhost 0.0.0.0 ::1`
3. Скопировать сертификаты для ssh в модуль lti_auth (необходимо для сервера на python) `cp ./key.pem ./lti_auth/key.pem & cp ./cert.pem ./lti_auth/cert.pem`
4. Создать и заполнить файл `.env`
5. Запустить проект `docker-compose up`


# Переменные окружения

См. `lti_auth.src.lti_auth.settings.settings.py` - создается объект настроек из `.env` файла

Там заданы дефолтные значения + дано краткое описание, за что именно отвечает та или иная настройка

Что настаивал я для запуска:
 - JWT_SECRET - секрет, который используется для подписания `jwt` токена в cookie
 - JWT_COOKIE_NAME - название куки, в которой будет лежать `jwt` токен
 - JWT_TASK_ID_PARAM_NAME - название параметра в payload `jwt` токена для `id` упражнения
 - JWT_USER_ID_PARAM_NAME - название параметра в payload `jwt` токена для `lms_user_id` пользователя
 - JWT_IS_TRIED_PARAM_NAME - название параметра в payload `jwt` токена для отображения информации о том, что пользователь ранее уже успешно решил данное упражнение
 - NGINX_HOST_NAME - хост в `url`, с которого редиректит `nginx` (необходимо сервису `lti_auth` для замены хоста в `url`, по которому перенаправляет запрос `nginx`, чтобы успешно проходить проверку `lti-запроса`). Например, чтобы локально тестировать, указывать в переменной `localhost`, и в адресе сервиса в `moodle` также указывать url через `localhost`
 - SESSION_SECRET_KEY - секрет, который мы кладём в moodle (по дефолту `secretkey`). Должен быть только из букв и цифр
 - SESSION_PUBLIC_KEY - публичный ключ, который мы кладем в moodle (по дефолту `publickey`). Должен быть только из букв и цифр


# Разработка на Python

Открываем lti_auth, как отдельный проект в ide и ведём разработку, как с самостоятельным проектом

## Линтеры и статические анализаторы кода

В `Pycharm` файл `README.md` подсвечивает возможность выполнения команд -> можно без прекоммитера удобно выполнять
 команды ниже. Эти же команды продублированы в `README.md`, расположенном в папке lti_auth

1. `python -m ruff check --select I --select T20 --select COM  --select B --exclude B008 --select F --select E --select W --select N --select C90  --fix src`
2. `python -m ruff format src`
3. `python -m mypy --install-types --non-interactive --show-error-context --show-column-numbers --pretty src`
4. `python -m deptry src` - игнорим `python-multipart`, он нужен для `fastapi`


# Подключение к moodle

В nginx задан url для `lti_auth` через суффикс `/python_app/`. То есть, например, локально мы хотим сходить в наш `lti_auth` - для этого мы должны прописать url `https://localhost/python_app/<some_python_uri>/`

В приложении `lti_auth` реализована ручка `/public/v1/lti/`. Именно эту ручку нужно вставлять в moodle, вместе с хостом и префиксом приложения. Например, локально получится `https://localhost/python_app/public/v1/lti/`
