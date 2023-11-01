### Setup ENV

look .env.example to see all required env variables


JSON_FILE_PATH - database is json file, so you need to specify file location


### To simply run application use docker

install docker on your system

use docker to run application
docker-compose build && docker-compose up


### Manual run application and tests

install pipenv

```bash
pip install pipenv
```

create virtual environment

```bash
pipenv install
```

activate environment

```bash
pipenv shell
```
run tests

```bash
pytest app/tests/test_services.py
```

run application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
```

visit documentation about API

```http request
http://localhost/docs#
```