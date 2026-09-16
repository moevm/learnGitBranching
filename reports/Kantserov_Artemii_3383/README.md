# Автотесты Learn Git Branching — Канцеров Артемий, группа 3383

Работа для заданий 9–16 курса Learn Git Branching. Реализованы все 32 описанных тест-кейса: по два позитивных и два негативных сценария для каждого уровня.

## Покрытые уровни

| № | ID | Название |
|---:|---|---|
| 9 | `move1` | Введение в Cherry-pick |
| 10 | `move2` | Введение в интерактивный Rebase |
| 11 | `mixed1` | Выберем один коммит |
| 12 | `mixed2` | Жонглируем коммитами |
| 13 | `mixed3` | Жонглируем коммитами №2 |
| 14 | `mixed4` | Git tag |
| 15 | `mixed5` | Git describe |
| 16 | `advanced1` | Rebase over 9000 раз |

Подробные предусловия, шаги и ожидаемые результаты находятся в [TEST_CASES.md](TEST_CASES.md).

## Структура запуска

Требуемые три контейнера описаны в `docker-compose.tests.yml` в корне репозитория:

1. `selenium-hub` — Selenium Grid;
2. `chrome` — браузер из образа `selenium/node-chrome`;
3. `tests` — Python-контейнер с `pytest` и тестами.

Для каждого уровня создан отдельный файл `tests/test_level_*.py`, а повторяющиеся действия вынесены в `tests/pages/base_page.py` и Page Object `tests/pages/learn_git_page.py`.

## Быстрый запуск напрямую

Для проверки без Moodle достаточно Docker и доступа в интернет:

```bash
docker compose -f docker-compose.tests.yml up --build --abort-on-container-exit --exit-code-from tests
```

По умолчанию тесты откроют русскую версию `https://learngitbranching.js.org/`. Ожидаемый итог:

```text
32 passed
```

Интерфейс запущенного Chrome доступен через noVNC: `http://localhost:7900`.

После прогона контейнеры можно остановить командой:

```bash
docker compose -f docker-compose.tests.yml down
```

## Запуск через курс Moodle

1. Скопировать `.env.tests.example` в `.env.tests`.
2. Заполнить в `.env.tests` значения `MOODLE_USERNAME` и `MOODLE_PASSWORD`.
3. При необходимости уточнить `MOODLE_ACTIVITY_NAME` или задать прямую ссылку на элемент курса в `MOODLE_ACTIVITY_URL`.
4. Выполнить ту же команду с файлом `docker-compose.tests.yml`.

Если `MOODLE_COURSE_URL` заполнен, тесты авторизуются в Moodle, открывают курс и переходят к элементу LearnGitBranching. Если переменная пуста, используется `TARGET_URL`.

Файл `.env.tests` исключён из Git. Логин и пароль не записываются в тесты и не выводятся в отчёт.

## Выборочный запуск

Только позитивные сценарии:

```bash
docker compose -f docker-compose.tests.yml run --rm tests pytest -m positive
```

Только негативные сценарии:

```bash
docker compose -f docker-compose.tests.yml run --rm tests pytest -m negative
```

Один уровень, например задание 9:

```bash
docker compose -f docker-compose.tests.yml run --rm tests pytest -k level_09
```

Для отладки без Grid поддержан локальный WebDriver: установить зависимости из
`tests/requirements.txt` и запустить pytest с `SELENIUM_REMOTE_URL=local`. Этот режим
не заменяет итоговый контейнерный запуск, а нужен только для быстрой разработки.
