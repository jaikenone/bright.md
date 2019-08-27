# bright.md

Timebox: 4 hours
Create a micro-service with the following:

* A User rest Resource that allows clients to create, read, update, delete a user or a list of users.
* You can use a database of your choice but it's also fine to just use a map or dictionary in memory to keep track of users by their ids.
* Use structured logging
* Add Metrics (such as dropwizard, codahale, or prometheus to time routes)
* Write unit tests for the service.
* Generate a code coverage report (for Java you can use the jacoco-maven-plugin for unit test coverage).
* If you are using Java take a look at: https://www.dropwizard.io/1.3.5/docs/getting-started.html
* The user JSON can just be id, first name, last name, zip code, and email address. If Java, the User class should be immutable.

You can use Java, GoLang, or Python for this exercise.

## Requirements
* Docker
* Docker-compose
* pip
* python 3.7

## Build and Run

### Postgres container
```
$ docker-compose up --build -d
```

### Virtualenv
```
$ cd bright
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Start Server
```
$ export POSTGRES_USER=test && \
  export POSTGRES_PASSWORD=password && \
  export POSTGRES_HOST=localhost && \
  export POSTGRES_PORT=5432 && \
  export POSTGRES_DB=bright && \
  export FLASK_APP=app.py && \
  flask run
```

## Examples

### Create
Post data is dictionary for new user or a list of dictionary for new users.
```
$ curl -XPOST -H "Content-type: application/json" -d '[{"first_name": "Leto", "last_name": "Atreides", "zip_code": "11111", "email": "leto@caladan.com"}, {"first_name": "Jessica", "last_name": "", "zip_code": "11111", "email": "paul@caladan.com"}, {"first_name": "Paul", "last_name": "Atreides", "zip_code": "11111", "email": "paul@caladan.com"}]'  '127.0.0.1:5000/user/create'
```
### Read
Read all or a list of users (example: /1 or /3,5).
```
$ curl '127.0.0.1:5000/user'
```
### Update
Update one user or a list of users.
```
$ curl -X 'PATCH' -H "Content-type: application/json" -d '[{"id": 1, "zip_code": "11111"},{"id": 2, "zip_code": "11111"}, {"id": 3, "zip_code": "11111"}]' '127.0.0.1:5000/user/update'
```
### Delete
Delete one user or a list users (example: /1 or /3,5).
```
$ curl -X "DELETE" '127.0.0.1:5000/user/delete/1'
```

## Test
Run all test.
```
$ py.test
```
Sample results
```
============================================ test session starts =============================================
platform darwin -- Python 3.7.3, pytest-5.1.1, py-1.8.0, pluggy-0.12.0
rootdir: /Users/pwong/ownCloud/Code/bright.md/bright
collected 7 items

tests/test_routes.py .......                                                                           [100%]

============================================= 7 passed in 5.13s ==============================================
```

## Coverage
Test test coverage.
```
$ coverage run --source bright -m pytest
$ coverage report
```
Sample results
```
Name                   Stmts   Miss  Cover
------------------------------------------
__init__.py               22      0   100%
app.py                    21     21     0%
config.py                  7      0   100%
models.py                  9      0   100%
routes.py                 64     11    83%
tests/__init__.py          0      0   100%
tests/conftest.py         23      0   100%
tests/test_routes.py      43      0   100%
------------------------------------------
TOTAL                    189     32    83%
```

