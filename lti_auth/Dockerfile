FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.8.3
# set versions

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app

CMD ["uvicorn", "lti_auth.app:app", "--host", "0.0.0.0", "--port", "80"]

