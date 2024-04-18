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

См. `src.settings.settings.py` - создается объект настроек из `.env` файла

Там заданы дефолтные значения + дано краткое описание, за что именно отвечает та или иная настройка


# Разработка на Python

Открываем lti_auth, как отедльный проект в ide и ведм разработку, как с самостоятельным проектом

## Линтеры и статические анализаторы кода

В `Pycharm` файл `README.md` подсвечивает возможность выполения команд -> можно без прекоммитера удобно выполнять
 команды ниже. Эти же команды продублированы в `README.md`, расположенном в папке lti_auth

1. `python -m ruff check --select I --select T20 --select COM  --select B --exclude B008 --select F --select E --select W --select N --select C90  --fix src`
2. `python -m ruff format src`
3. `python -m mypy --install-types --non-interactive --show-error-context --show-column-numbers --pretty src`
4. `python -m deptry src` - игнорим `python-multipart`, он нужен для `fastapi`
