# auto-ria-scrapping

## About

Program for periodic scrapping data about cars from auto.ria.com

## Functionality

1. Collecting information about cars at auto.ria.com
2. Adding info about cars to PostgresDB
3. Dumping data from DB to JSON-file
4. Scheduling for collecting and dumping data

## Technologies used

PostgresDB, SQLAlchemy + Alembic, Celery + Redis, Selenium, Docker compose

## How to run

### Prerequests
Dokcer must be installed

1. Clone this repository:
```shell
git clone https://github.com/ant-komarov/auto-ria-scrapping
```
2. Create new .env-file from .env.sample in project root directory and fill data
3. In console input:
```shell
docker-compose up --build
```

## Shutdown

```shell
ctrl + C 
```

