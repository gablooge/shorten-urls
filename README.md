# Shorten URLs
## Run locally

### using docker

- build and run the docker for the development

    ``` bash
    # run database
    docker compose -f docker-compose.dev.yaml up db -d --build
    # run apps
    docker compose -f docker-compose.dev.yaml up apps -d --build

    # run all services
    docker compose -f docker-compose.dev.yaml up -d --build
    ```

- Open the `http://localhost:8000/admin/`

- unit test

    ```bash
    docker compose -f docker-compose.dev.yaml up test --build
    ```

### run on host machine

- Once defined (by any convenient means), install the projects dependencies via virtualenv,

    ``` bash
    # From project root directory

    # Using python venv (Not Recommended)
    python3 -m venv venv
    source ./venv/bin/activate

    # Recommended to use poetry
    # Install dependencies
    poetry install --no-root
    # or
    poetry update

    # when failing to install the dependencies
    poetry export --output requirements-dev.txt --with dev
    pip install -r requirements-dev.txt

    # when got ImportError: cannot import name 'appengine' from 'urllib3.contrib'
    pip install urllib3==1.26.15 requests-toolbelt==0.10.1
    ```

- Run Local

    ```bash
    # export the variables for database if using external database
    export DEBUG=true
    export DB_HOST=localhost

    poetry run python manage.py runserver
    ```

- Go to the Django Shell

    ```bash
    poetry run python manage.py shell
    ```

- Database Migrations

    ```bash
    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    ```

- Lint Testing

    For lint testing run the following command in the project root

    ```bash
    # flake8
    poetry run flake8
    # isort check
    poetry run isort . --check-only

    # liccheck
    poetry export --output requirements.txt --without dev
    poetry run liccheck -s pip-licenses-strategy.ini

    # bandit
    poetry run bandit -c .bandit.yml -r *

    # safety
    wget https://github.com/pyupio/safety-db/raw/master/data/insecure_full.json
    wget https://github.com/pyupio/safety-db/raw/master/data/insecure.json
    poetry run safety check --full-report
    ```

- Unit Test

    For unit testing run the following command in the project root

    ```bash
    export DB_HOST=127.0.0.1 # when failing make sure to use postgres user
    poetry run python manage.py test --exclude=e2e --settings=mainapps.settings.dev
    ```

- E2E Tests

    ```bash
    export DB_HOST=127.0.0.1 # when failing make sure to use postgres user
    poetry run python manage.py test e2e --settings=mainapps.settings.dev
    ```

- Available commands

    Generate user

    ```bash
    poetry run python manage.py generate_user
    ```

### Generate OpenAPI spec

```bash
poetry run python manage.py spectacular --color --file spec/openapi.yaml \
    --settings=mainapps.settings.dev

# open using docker swagger viewer on http://localhost:8888/
docker run -p 8888:8080 \
    -e SWAGGER_JSON=/schema.yaml \
    -v ${PWD}/spec/openapi.yaml:/schema.yaml \
    swaggerapi/swagger-ui
```

### Erasing all data

```bash
# run all data including the database
docker compose -f docker-compose.dev.yaml down -v
```
