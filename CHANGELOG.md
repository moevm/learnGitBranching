# 27.02.2024 №1

Приложение разбито на 2 части: фронт и сервер, для этого исходное приложение
 было склонировано в два модуля.

# 27.02.2024 №2

В исходном приложении был вычленен код, который отвечает за:
- Получение заданий
- Проверку решения задания

Следом в серверном приложении было создано API для предоставления доступа
 к ним по сети.

Затем в фронтенд-приложении эти куски кода были заменены на вызовы API
 серверного приложения


# 27.02.2024 №3

В фронтенд-приложении была добавлена поддержка query-параметра `level_id`,
 который позволяет без ручного выбора сразу открывать уровень с выбранным
 `level_id`. 

Доступные на данный момент `level_id`:
- intro + индекс от 1 до 4
- advanced1
- mixed + индекс от 1 до 5
- rampup + индекс от 1 до 6
- rebase + индекс от 1 до 2
- remote + индекс от 1 до 16


# 27.02.2024 №4

В серверном приложении было реализовано получение fronted-сборки по API, 
 при этом обязательно должен быть указан параметр `level_id`, иначе
 будет отправлена ошибка 404
