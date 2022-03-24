FROM python:3.9

RUN mkdir /app

COPY . /app
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN pip3 install poetry 
RUN poetry config virtualenvs.create false
RUN poetry install 