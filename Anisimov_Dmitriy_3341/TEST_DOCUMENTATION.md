# Анисимов Дмитрий, гр. 3341
# Тестовая документация: Learn Git Branching

## Объект тестирования

Сайт:

```text
https://learngitbranching.js.org/?locale=ru_RU
```

Проверяется русская версия тренажёра Learn Git Branching. Тесты запускают сайт, пропускают стартовые инструкции, выбирают нужный уровень, вводят команды в консоль тренажёра и проверяют результат через интерфейс и внутренние debug-функции сайта.

## Инструменты

- Python
- pytest
- Selenium Remote WebDriver
- Docker Compose
- `selenium/hub`
- `selenium/node-chrome`
- отдельный контейнер `tests` с pytest-тестами

## Общие предусловия

- Установлен Docker.
- Есть доступ к интернету.
- Сайт Learn Git Branching открывается.
- Тесты запускаются из корня проекта.

## Запуск

```powershell
docker compose up --build --abort-on-container-exit
```

Для просмотра браузера во время выполнения тестов:

```text
http://localhost:7900
```

Дополнительный ввод при открытии просмотра не нужен.

## Структура тестов

```text
tests/e2e/
```

Каждый тест-кейс находится в отдельном файле. В названии файла используется:

- `p` — позитивный сценарий;
- `n` — негативный сценарий;
- `p1`, `p2` — несколько позитивных проверок внутри одной темы.

## Назначение основных каталогов и файлов

Основная структура проекта:

```text
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
README.md
Инструкция.md
tests/
```

Назначение основных каталогов и файлов:

- `Dockerfile` — описывает контейнер `tests`, внутри которого устанавливаются Python-зависимости и запускается pytest;
- `docker-compose.yml` — описывает три контейнера: Selenium Hub, Chrome node и контейнер с тестами;
- `requirements.txt` — содержит библиотеки, необходимые для запуска автотестов;
- `pytest.ini` — хранит настройки pytest и зарегистрированные маркеры тестов;
- `README.md` — краткая инструкция по запуску проекта;
- `Инструкция.md` — пояснение по Docker и работе с контейнерами;
- `tests/` — каталог с автотестами, фикстурами и Page Object классом;
- `tests/e2e/` — тестовые сценарии, каждый файл соответствует отдельному тест-кейсу;
- `tests/pages/` — вспомогательные классы для работы со страницей Learn Git Branching.

### Page Object классы

В проекте используется Page Object подход. Общая логика работы с сайтом вынесена в файл:

```text
tests/pages/learn_git_branching_page.py
```

Класс `LearnGitBranchingPage` отвечает за повторяющиеся действия на сайте:

- открытие нужного уровня;
- пропуск стартовых и уровневых инструкций;
- выбор уровня через интерфейс;
- ввод команд в консоль тренажёра;
- ожидание завершения анимаций и команд;
- проверка успешного прохождения уровня;
- получение текста графа коммитов для проверок.

Благодаря этому сами тесты в `tests/e2e/` остаются короткими: в них описан сценарий конкретного тест-кейса, а техническая работа с интерфейсом находится в Page Object.

### Фикстуры pytest

Фикстуры расположены в файле:

```text
tests/conftest.py
```

Основные фикстуры:

- `selenium_url` — получает адрес Selenium Grid из переменной окружения `SELENIUM_REMOTE_URL`;
- `driver` — создаёт Selenium Remote WebDriver, подключённый к Chrome node в Docker;
- `lgb` — создаёт объект `LearnGitBranchingPage`, через который тесты работают с сайтом.

Перед созданием браузера выполняется ожидание готовности Selenium Grid. Это нужно, чтобы тесты не стартовали раньше, чем контейнеры `selenium/hub` и `selenium/node-chrome` будут готовы принимать команды.

## Реализованные тест-кейсы

| ID | Файл | Уровень сайта | Тип | Проверка |
|---|---|---|---|---|
| TC-01-P | `test_tc_01_p_commit.py` | `intro1` | Позитивный | Два `git commit` успешно проходят первый уровень. |
| TC-01-N | `test_tc_01_n_invalid_commit.py` | `intro1` | Негативный | Некорректная команда `git commmit` не меняет граф и не проходит уровень. |
| TC-02-P1 | `test_tc_02_p1_branch.py` | `intro2` | Позитивный | `git branch bugFix` создаёт новую ветку. |
| TC-02-P2 | `test_tc_02_p2_checkout_branch.py` | `intro2` | Позитивный | `git checkout bugFix` переключает HEAD на созданную ветку и завершает уровень. |
| TC-02-N | `test_tc_02_n_checkout_unknown_branch.py` | `intro2` | Негативный | Переход на несуществующую ветку не меняет граф. |
| TC-03-P1 | `test_tc_03_p1_merge_level.py` | `intro3` | Позитивный | Полный сценарий merge проходит уровень. |
| TC-03-P2 | `test_tc_03_p2_merge_pointers.py` | `intro3` | Позитивный | После merge остаются видимыми `main`, `bugFix` и `HEAD`. |
| TC-03-N | `test_tc_03_n_wrong_merge_direction.py` | `intro3` | Негативный | Merge в неправильном направлении не засчитывает уровень. |
| TC-04-P1 | `test_tc_04_p1_rebase_level.py` | `intro4` | Позитивный | Полный сценарий rebase проходит уровень. |
| TC-04-P2 | `test_tc_04_p2_rebase_order.py` | `intro4` | Позитивный | После rebase история меняется и уровень засчитывается. |
| TC-04-N | `test_tc_04_n_wrong_rebase_direction.py` | `intro4` | Негативный | Rebase в неправильном направлении не засчитывает уровень. |
| TC-05-P1 | `test_tc_05_p1_detached_head_checkout_hash.py` | `rampup1` | Позитивный | `git checkout C4` переводит HEAD в detached-состояние и проходит уровень. |
| TC-05-P2 | `test_tc_05_p2_detached_head_other_hash.py` | `rampup1` | Позитивный | После detached HEAD можно перейти на другой коммит по hash. |
| TC-05-N | `test_tc_05_n_checkout_branch_instead_of_hash.py` | `rampup1` | Негативный | `git checkout bugFix` не создаёт нужное detached-состояние. |
| TC-06-P1 | `test_tc_06_p1_relative_ref_caret.py` | `rampup2` | Позитивный | `git checkout bugFix^` переходит на родительский коммит и проходит уровень. |
| TC-06-P2 | `test_tc_06_p2_relative_ref_tilde.py` | `rampup2` | Позитивный | `git checkout bugFix~1` даёт тот же корректный результат. |
| TC-06-N | `test_tc_06_n_relative_ref_too_far.py` | `rampup2` | Негативный | Слишком дальняя ссылка `bugFix~5` не проходит уровень. |
| TC-07-P1 | `test_tc_07_p1_relative_refs_force_branches.py` | `rampup3` | Позитивный | Полный сценарий с `git branch -f` проходит уровень. |
| TC-07-P2 | `test_tc_07_p2_branch_force_keeps_history.py` | `rampup3` | Позитивный | `git branch -f main C6` не удаляет историю коммитов. |
| TC-07-N | `test_tc_07_n_branch_without_force.py` | `rampup3` | Негативный | Попытка переместить существующую ветку без `-f` не проходит уровень. |
| TC-08-P1 | `test_tc_08_p1_reset_local_commit.py` | `rampup4` | Позитивный | `git reset HEAD~1` отменяет локальный коммит. |
| TC-08-P2 | `test_tc_08_p2_revert_pushed_commit.py` | `rampup4` | Позитивный | `git revert HEAD` для `pushed` завершает уровень после reset на `local`. |
| TC-08-N | `test_tc_08_n_reset_pushed_commit.py` | `rampup4` | Негативный | Reset на ветке `pushed` является неправильной стратегией и не проходит уровень. |

## Ожидаемый результат полного запуска

```text
23 passed
```

Последний полный Docker-прогон:

```text
23 passed in 1284.62s (0:21:24)
```
