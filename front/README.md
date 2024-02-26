# Как запустить nestjs приложение в docker?

### 1. Зпуситить приложение в докере
```bash
$ docker-compose up
```


# Как запустить nestjs приложение в консоли?


### 1. Установить зависимости
```bash
$ npm i
```


### 2. Запустить приложение
```bash
$ npm run start
```


# Список ручек, которые есть и что они делают (кратко)
- `/send-command/` - принимает на вход уровень + комманду, применяет её и возвращает информацию о том, завершен ли уровень + вывод гита от выполнения этой команды
- `/reset-level/` - принимает на вход уровень и сбрасивает его состояние, чтобы можно было начать его выполнение заново


# Как можно проверить работу nestjs приложения?


### 1. Отправить POST запрос на http://localhost:3000/send-command/ с телом:
```json
{
  "command": "git reset HEAD~1;git checkout pushed;git revert HEAD",
  "levelType": "rampup",
  "levelIndex": 3
}
```

### 2. Проверить резульаты:

Увидеть тело ответа
```json
{
  "result": true,
  "gitMessage": "",
  "message": "level completed"
}
```
Также в консоли будет выведено сообщение вида:
```
Выполнен ли уровень:
level completed
```

### 3. Отправить комманды, не приводящие к решению

Пример тела запроса:
```json
{
    "command": "git commit;git commit; git log;",
    "levelType": "rampup",
    "levelIndex": 3
}
```

Будут возвращаться ответы вида:
```json
{
  "result": false,
  "gitMessage": "Результат команды git log:\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C5\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C4\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C3\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C1\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C0\n",
  "message": "not completed"
}
```
Также в консоли будет выводиться сообщение вида (с внесенными изменениями, посланной командой):
```
Выполнен ли уровень:
not completed
Результат команды git log:
Author: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C5
Author: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C4
Author: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C3
Author: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C1
Author: Peter Cottle<br/>Date: Fri Dec 08 2023 23:24:01 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C0
```


### 4. Отправить POST запрос на ручку http://localhost:3000/reset-level с телом:
{
"levelIndex": 3,
"levelType": "rampup"
}

Будут возвращаться ответы:
```json
{
  "result": "success",
  "message": "level reset"
}
```

### 5. Отправить комманду `git log` в ручку `/send-command/` и удостовериться, что сделанные коммиты сбросились
Тело запроса:
```json
{
    "command": "git log;",
    "levelType": "rampup",
    "levelIndex": 3
}
```

Результат:

```json
{
    "result": false,
    "gitMessage": "Результат команды git log:\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:31:17 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C3\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:31:17 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C1\nAuthor: Peter Cottle<br/>Date: Fri Dec 08 2023 23:31:17 GMT+0300 (Москва, стандартное время)<br/><br/>Quick commit. Go Bears!<br/><br/>Commit: C0\n",
    "message": "not completed"
}
```
