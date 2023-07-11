FROM python:alpine
COPY ./ ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
CMD ["poetry", "run", "start", ".env"]