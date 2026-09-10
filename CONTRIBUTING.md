# Contribution Guide

Development of this project has been setup to be done from VSCodium. This guide covers how to
develop Centurion ERP locally. Further development documentation relevant to the code itself is available at
<https://nofusscomputing.com/projects/centurion_erp/development/>.

The following assumptions are made in relation to developing Centurion ERP:

- You can code in python.

- You are familiar with Github.

- You are familiar with git

- You are familiar with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

- That development will be conducted within VSCodium / VSCode. _(Optional, not really required. Only here as everything setup to work with it)_

- You know what a `make` file is.

- You know how to operate you local machines package manager.

- You are familiar with docker. _(Optional, only required if doing Docker "things")_

- You are familiar with kubernetes. _(Optional, only required if doing Kubernetes "things")_

- Development is being conducted from linux. If you are stuck using spyware (You know who you are mister OS that shall remain un-named), then... shit. All commands and thing-a-ma-jiggies have been written for linux. They may work on your spyware (You know who you are mister OS that shall remain un-named) host, or they may not. We **won't** be changing this.

If these assumptions are incorrect in relation to you, the onus is upon you to rectify these as this is beyond the scope of this guide.


## First steps

You are encouraged to do the following as they will assist in the development workflow:

- Read Centurion ERP docs <https://nofusscomputing.com/projects/centurion_erp/>. **Yes** all of it.

- Make yourself familiar with the code base

- Read / View open Issues.

    **Note:** We always have an epic open titled _"Planning Document: [whatever next version is]."_ There is one always part of a milestone prefixed with `Next Release - `. This epic is a working document for every release and notates the current goals, direction etc.

- Read / View open Pull/Merge requests. This provides insight into many different areas.

If you **are not a developer** you can still contribute. You can do this by using Centurion ERP and reporting any issues with it.


## Development

> [!IMPORTANT]
>
> It is a requirement that CI Jobs pass on Github. If any **required** CI job fails or does not run, you will be required to fix this. In your forked repo of Centurion ERP, activate github actions. Then, every time you push a commit the CI jobs will run and be reported on the PR.

This section details how to setup your development environment.

- Fork Centurion-erp, so you have a copy.

- Clone your fork of the repository

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

> [!WARNING]
>
> Ensure that there is **no** development server running before creating fixtures.

``` bash

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
> Common `make` commands are `make prepare-python` and `make pip`.

Included within the root of the repository is a makefile that can be used during
development to check/run different items as required. The following make targets
are available:

- `prepare-python`

    _Sets up the python virtual environment ready for dev._

- `prepare-ui`

    _Clones the Centurion UI locally. Enables viewing your dev work in the UI._

- `build`

    _Build Centurion ERP wheel._

- `build-pip`

    _Compiles the pip files in the `tools/` directory._

- `docs-lint`

    _Lints the markdown documents within the docs directory for formatting
    errors that MkDocs may/will have an issue with. It is quicker to lint the docs locally if you are working on them._

- `fixtures`

    _Generates the database test fixtures (`app/fixtures/`)._

- `pip`

    _Synchronises pip packages within the virtual env. Enables you to update the python dependencies if they have been updated in dev without having to recreate the environment._

- `clean`

    _Cleans up build artifacts and removes the python virtual environment._


## Testing


> [!IMPORTANT]
> **"Requirement"**
>
> All models **are** to have tests written for them, including testing between
> dependent models.

See the [testing documentation](https://nofusscomputing.com/projects/centurion_erp/development/testing/)
for further information.


## Tips / Handy info

- To obtain a list of models _(in the same order as the file system)_ using the
    db shell `python3 manage.py dbshell`, run the following SQL command:

    ``` sql

    SELECT model FROM django_content_type ORDER BY app_label ASC, model ASC;

    ```

- To build and run a single Centurion image:

    ``` bash

    cd app

    docker build . --tag centurion-erp:dev

    docker run -d --rm -v ${PWD}/db.sqlite3:/app/db.sqlite3 -p 8002:8000 --name app centurion-erp:dev

    ```

- Page speed tests

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

