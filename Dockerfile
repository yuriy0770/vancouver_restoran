FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY manage.py .
COPY config/ ./config/
COPY res/ ./res/
COPY reservations/ ./reservations/
COPY users/ ./users/
COPY templates/ ./templates/
COPY static/ ./static/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]