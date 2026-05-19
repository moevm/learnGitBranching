# Learn Git Branching: 4 итерация

Автотесты для заданий 9-16 сайта Learn Git Branching:

```text
https://learngitbranching.js.org/?locale=ru_RU
```

Покрыты уровни:

- `move1` — Введение в Cherry-pick;
- `move2` — Введение в интерактивный Rebase;
- `mixed1` — Выберем один коммит.;
- `mixed2` — Жонглируем коммитами.
- `mixed3` — Жонглируем коммитами №2;
- `mixed4` — git tag;
- `mixed5` — Git describe;
- `advanced1` — Rebase over 9000 раз.

Всего реализовано 32 теста: по 2 позитивных и 2 негативных на каждый уровень.

## Запуск

```powershell
docker compose up --build --abort-on-container-exit
```

Ожидаемый результат:

```text
32 passed
```

Для просмотра браузера во время запуска:

```text
http://localhost:7900
```
