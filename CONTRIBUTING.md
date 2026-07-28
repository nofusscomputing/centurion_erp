# Contribution Guide

Development of this project has been setup to be done from VSCodium. This guide
covers the requirements, how to start a local development server, the available
`make` targets, linting, testing and running the stack under Docker.

Further development documentation relevant to the code itself is available at
<https://nofusscomputing.com/projects/centurion_erp/development/>.


## Requirements

The following additional requirements need to be met:

- `npm` is installed. _required for `markdown` linting_

    ``` bash

    sudo apt install -y --no-install-recommends npm

    ```

- Setup of the remaining requirements is done with `make prepare-python`. This
    initialises the git submodules and sets up the Python virtual environment.

- **ALL** linting must pass for a merge to be conducted (`make lint`).


## Development Environment Setup

This section details how to setup your development environment.

- Clone the repository

- Setup the python environment

    ``` bash

    # Enter repository directory
    cd centurion-erp

    # Setup python
    make prepare-python

    ```

- Open Repository in VSCodium

    ``` bash

    . codium

    ```

    VSCodium will open with centurion-erp loaded and is ready for development.

    > [!TIP]
    >
    > VSCodium must be installed for the above command to work. If you use VSCode instead use `. code`.

- Return to the terminal to start the development server

    ``` bash

    # Activate the python venv
    source .venv/bin/activate

    # Enter the app dir
    cd app

    # Start the dev server, viewable at http://127.0.0.1:8002
    python manage.py runserver 8002

    # Run any migrations, if required
    python manage.py migrate

    # Create a super user, if required
    python manage.py createsuperuser

    ```

## Notes

If you have made model changes, generate the migrations and regenerate the
database test fixtures (migrations are disabled for tests, so the fixtures are
what the test suite relies upon):

``` bash

python manage.py makemigrations

# Only required if not already setup
make prepare-python

# Generates the DB test fixtures
# app/fixtures/fresh_db.json <- Dont commit this file as the only thing that should change is the date
# app/fixtures/fresh_db.sql <- only commit this file if there are actual changes i.e. Tables are different or the django_migrations count has changed.
make fixtures

```

To update the code-highlight stylesheet run:

``` bash

pygmentize -S default -f html -a .codehilite > project-static/code.css

```


## Makefile


> [!TIP]
> Common `make` commands are `make prepare-python` then `make docs` and
> `make lint`.

Included within the root of the repository is a makefile that can be used during
development to check/run different items as required. The following make targets
are available:

- `prepare-python`

    _Sets up the python virtual environment._

- `docs`

    _Builds the docs and places them within a directory called `build`, which
    can be viewed within a web browser._

- `lint`

    _Conducts all required linting._

    - `docs-lint`

        _Lints the markdown documents within the docs directory for formatting
        errors that MkDocs may/will have an issue with._

- `fixtures`

    _Generates the database test fixtures (`app/fixtures/`)._

- `pip-file`

    _Compiles the pip files in the `tools/` directory._

- `pip`

    _Synchronises pip packages. Note: uses the current python, i.e. if a virtual
    env is activated it will sync packages within the virtual env._

- `clean`

    _Cleans up build artifacts and removes the python virtual environment._


## Linting


All linting must pass before a merge can be conducted:

``` bash

make lint

```
> [!TIP]
>
> In your forked repo of Centurion ERP, if you activate github actions, every time you push a commit the CI lint job will run.

## Testing


> [!IMPORTANT]
> **"Requirement"**
>
> All models **are** to have tests written for them, including testing between
> dependent models.

See the [testing documentation](https://nofusscomputing.com/projects/centurion_erp/development/testing/)
for further information.


## Docker


To build and run a single Centurion image:

``` bash

cd app

docker build . --tag centurion-erp:dev

docker run -d --rm -v ${PWD}/db.sqlite3:/app/db.sqlite3 -p 8002:8000 --name app centurion-erp:dev

```


## Page speed tests


To run page speed tests (requires a working prometheus and grafana setup) use
the following:

``` bash

clear; \
  K6_PROMETHEUS_RW_TREND_STATS="p(99),p(95),p(90),max,min" \
  K6_PROMETHEUS_RW_SERVER_URL=http://<prometheus url>:9090/api/v1/write \
  BASE_URL="http://127.0.0.1:8002" \
  AUTH_TOKEN="<api token of superuser>" \
  k6 run \
    -o experimental-prometheus-rw \
    --tag "commit=$(git rev-parse HEAD)" \
    --tag "testid=<name of test for ref>" \
    test/page_speed.js

```


## Tips / Handy info


- To obtain a list of models _(in the same order as the file system)_ using the
    db shell `python3 manage.py dbshell`, run the following SQL command:

    ``` sql

    SELECT model FROM django_content_type ORDER BY app_label ASC, model ASC;

    ```
