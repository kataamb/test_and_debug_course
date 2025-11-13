FROM python:3.13-slim

WORKDIR .

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Скопируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без dev)
RUN poetry install --no-root --without dev

# Копируем код
COPY ./abstract_repositories ./abstract_repositories
COPY ./controllers ./controllers
COPY ./core ./core
COPY ./dto ./dto
COPY ./i_sql_builders ./i_sql_builders
COPY ./models ./models
COPY ./repositories ./repositories
COPY ./routers ./routers
COPY ./services ./services
COPY ./sql_builders ./sql_builders
COPY ./templates ./templates
COPY ./tests ./tests
COPY ./auth ./auth
COPY config.json log_config.json main.py service_locator.py ./

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



