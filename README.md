## HSEER

## Run locally

### using docker
- build and run the docker for the production

``` bash
docker-compose up -d --build
```
- Open the `http://localhost:9090/admin`

- unit test
```
docker-compose -f docker-compose.dev.yaml up --build --exit-code-from test test db
```

### run on host machine
- Once defined (by any convenient means), install the projects requirements via virtualenv,

``` bash
# From project root directory
python3 -m venv venv
source ./venv/bin/activate

# Install base requirements
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

- Run Local

```bash
# export the variables for database if using external database
export DB_PORT=55432
export DB_HOST=127.0.0.1
python manage.py runserver
```

- Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

- Lint Testing
For lint testing run the following command in the project root

```bash
flake8
```

- Unit Test

For unit testing run the following command in the project root

```bash
pytest
```
