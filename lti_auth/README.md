# Разработка

## Линтеры/форматеры/статические анализаторы кода

1. `python -m ruff check --select I --select T20 --select COM  --select B --exclude B008 --select F --select E --select W --select N --select C90  --fix src`
2. `python -m ruff format src`
3. `python -m mypy --install-types --non-interactive --show-error-context --show-column-numbers --pretty src`
4. `python -m deptry src`
