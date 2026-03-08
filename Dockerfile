FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY . /app

# Install dependencies from Pipfile.lock into system Python (non-interactive).
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000
