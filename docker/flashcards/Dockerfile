FROM python:3.10-alpine

COPY requirements /requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /requirements/development.txt
COPY pyproject.toml /pyproject.toml
