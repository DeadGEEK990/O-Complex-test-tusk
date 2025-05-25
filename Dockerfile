FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential libpq-dev && apt-get clean

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com

CMD ["sh", "-c", "\
    python manage.py migrate && \
    python manage.py createsuperuser --noinput || true && \
    python manage.py runserver 0.0.0.0:8000 \
"]