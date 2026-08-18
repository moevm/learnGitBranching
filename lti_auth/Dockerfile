# syntax=docker/dockerfile:1.7
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --retries 10 --timeout 120 poetry==1.8.3

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry export -f requirements.txt --output requirements.txt \
    && pip install --retries 10 --timeout 120 -r requirements.txt

COPY ./src /app

CMD ["uvicorn", "lti_auth.app:app", "--host", "0.0.0.0", "--port", "80"]
