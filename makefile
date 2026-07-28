.ONESHELL:

.SILENT:

# ANSI Terminal Colours

BLACK         := \033[30m
BLACK_BRIGHT  := \033[90m

BLUE          := \033[34m
BLUE_BRIGHT   := \033[94m

CYAN          := \033[36m
CYAN_BRIGHT   := \033[96m

GREEN         := \033[32m
GREEN_BRIGHT  := \033[92m

MAGENTA       := \033[35m
MAGENTA_BRIGHT := \033[95m

RED           := \033[31m
RED_BRIGHT    := \033[91m

RESET         := \033[0m

WHITE         := \033[37m
WHITE_BRIGHT  := \033[97m

YELLOW        := \033[33m
YELLOW_BRIGHT := \033[93m


# ANSI Terminal Background colours.
BG_BLACK          := \033[40m
BG_BLACK_BRIGHT   := \033[100m

BG_BLUE           := \033[44m
BG_BLUE_BRIGHT    := \033[104m

BG_CYAN           := \033[46m
BG_CYAN_BRIGHT    := \033[106m

BG_GREEN          := \033[42m
BG_GREEN_BRIGHT   := \033[102m

BG_MAGENTA        := \033[45m
BG_MAGENTA_BRIGHT := \033[105m

BG_RED            := \033[41m
BG_RED_BRIGHT     := \033[101m


# ANSI Terminal Text formatting
BOLD       := \033[1m
DIM        := \033[2m
ITALIC     := \033[3m
UNDERLINE  := \033[4m
BLINK      := \033[5m
REVERSE    := \033[7m
HIDDEN     := \033[8m
STRIKETHROUGH := \033[9m

RESET      := \033[0m
RESET_BOLD := \033[21m
RESET_DIM  := \033[22m
RESET_ITALIC := \033[23m
RESET_UNDERLINE := \033[24m
RESET_BLINK := \033[25m
RESET_REVERSE := \033[27m
RESET_HIDDEN := \033[28m
RESET_STRIKETHROUGH := \033[29m


PATH_VENV := ${PWD}/.venv

ACTIVATE_VENV :=. ${PATH_VENV}/bin/activate

#See dockerfile arg `PYTHON_VERSION` for current version
PYTHON_BIN    := python3.11

START_PWD     := ${PWD}

.PHONY: clean prepare docs ansible-lint lint test

prepare-git-submodule:
	git submodule update --init;
	git submodule foreach git submodule update --init;


prepare-python: prepare-git-submodule
	echo "${BLUE}Checking for Python Virtual Environment...${RESET}";
	if [ ! -f ${PATH_VENV}/bin/activate ]; then

		echo "    ${BLUE}Setting up Python Virtual Environment...${RESET}";

		${PYTHON_BIN} -m venv ${PATH_VENV} || echo "${RED}Failed to create Virtual Environment. ${RESET}";

		echo "    ${BLUE}Activating Python Virtual Environment...${RESET}";

		${ACTIVATE_VENV} || echo "${RED}Failed to activate Virtual Environment. ${RESET}";

		echo "    ${BLUE}Installing Python dependencies in Virtual Environment...${RESET}";

		pip install -r requirements_dev.txt || echo "${RED}Failed to install Python Dependencies in Virtual Environment. ${RESET}";

	else

		echo "    ${GREEN}Python Virtual Environment already setup. Nothing to do.${RESET}";

	fi;

		echo "    ${BLUE}prepare-python complete.${RESET}";


prepare-docs: prepare-git-submodule
	npm install markdownlint-cli2;
	npm install markdownlint-cli2-formatter-junit;
	cp -f "website-template/.markdownlint.json" ".markdownlint.json";
	cp -f "gitlab-ci/lint/.markdownlint-cli2.jsonc" ".markdownlint-cli2.jsonc";


markdown-mkdocs-lint: prepare-docs
	PATH=${PATH}:node_modules/.bin markdownlint-cli2 docs/*.md docs/**/*.md docs/**/**/*.md docs/**/**/**/*.md docs/**/**/**/**/**/*.md !docs/pull_request_template.md !CHANGELOG.md !gitlab-ci !website-template || true


docs-lint: markdown-mkdocs-lint


docs: docs-lint
	${ACTIVATE_VENV}
	mkdocs build --clean


fixtures:
	${ACTIVATE_VENV}
	mv app/db.sqlite3 app/db.sqlite3-current
	if [ ! -f app/db.sqlite3-current ]; then echo "failed to save current db"; exit 1; fi;
	python app/manage.py migrate;
	python app/manage.py dumpdata \
		--natural-foreign \
		--natural-primary \
		--exclude=contenttypes \
		--exclude=auth.permission \
		--exclude=access.centurionuser \
		--exclude=settings.usersettings \
		--indent 2 > app/fixtures/fresh_db.json;
	sqlite3 app/db.sqlite3 .dump | \
		grep -a -v 'INSERT INTO django_migrations' | \
		grep -a -v 'INSERT INTO django_content_type' | \
		grep -a -v 'INSERT INTO auth_permission' | \
		grep -a -v 'INSERT INTO settings_appsettings' | \
		grep -a -v 'INSERT INTO access_centurionuser' | \
		grep -a -v 'INSERT INTO settings_usersettings' | \
		grep -a -v 'CREATE UNIQUE INDEX' | \
		grep -a -v 'CREATE INDEX' \
		> app/fixtures/fresh_db.sql;
	rm -f app/db.sqlite3
	if [ ! -f app/db.sqlite3 ]; then cp app/db.sqlite3-current app/db.sqlite3; fi;
	if [ -f app/db.sqlite3 ]; then rm -f app/db.sqlite3-current; fi;



lint: markdown-mkdocs-lint


pip-file:
	pip-compile --upgrade tools/requirements.in -o requirements.txt -vv
	pip-compile --upgrade requirements.txt tools/requirements_production.in -o requirements_production.txt -vv
	pip-compile --upgrade requirements.txt requirements_production.txt tools/requirements_dev.in -o requirements_dev.txt -vv
	pip-compile --upgrade requirements.txt requirements_production.txt tools/requirements_docker.in -o requirements_docker.txt -vv

pip:
	pip-sync requirements_dev.txt -vv

test:
	pytest --cov-report xml:artifacts/coverage_unit_functional.xml --cov-report html:artifacts/coverage/unit_functional/ --junit-xml=artifacts/unit_functional.JUnit.xml app/**/tests/unit app/**/tests/functional



test-integration:
	export exit_code=0;
	cp pyproject.toml app/;
	sed -i 's|^source = \[ "./app" \]|source = [ "." ]|' app/pyproject.toml;
	cp -f requirements_dev.txt test/requirements_dev.txt;
	cd "${START_PWD}/test";
	if [ ! -n "$CENTURION_IMAGE_TAG" ]; then
		export CENTURION_IMAGE_TAG=$$(git log -1 --format=%H);
	fi
	if docker-compose up -d; then

		docker ps -a;

		chmod +x setup-integration.sh;

	
		if [ "0${GITHUB_SHA}"!="0" ]; then

			sudo chmod 777 -R "${START_PWD}/test"

		fi;


		if ./setup-integration.sh; then

			cd "${START_PWD}";

			ls -laR test/;

			docker exec -i centurion-erp sh -c 'rm -rf /app/artifacts/* /app/artifacts/.[!.]*';
			sleep 60;
			docker ps -a;
			curl --trace-ascii - http://localhost:8003/api;
			echo '--------------------------------------------------------------------';
			curl --trace-ascii - http://127.0.0.1:8003/api;


			docker logs centurion-erp;
			echo 'Starting integration tests.';
			pytest --override-ini addopts= --no-migrations --reuse-db --tb=long --verbosity=2 --showlocals --junit-xml="${START_PWD}/integration.JUnit.xml" app/*/tests/integration;
			echo 'Creating Coverage reports.';
			docker exec -i centurion-erp sh -c 'coverage combine; coverage report --skip-covered; coverage html -d artifacts/html/;';

		else

			cd "${START_PWD}";
			ls -la;

			echo 'Error: could not setup containers for testing';
			echo '';
			echo '';
			ls -lar "${START_PWD}/test";
			echo '';
			docker ps -a;
			docker logs centurion-erp-init > "${START_PWD}/test/volumes/log/docker-log-centurion-erp-init.log";
			docker logs centurion-erp> "${START_PWD}/test/volumes/log/docker-log-centurion-erp.log";
			docker logs postgres > "${START_PWD}/test/volumes/log/docker-log-postgres.log";
			docker exec -i postgres psql -Uadmin -c "\l" > "${START_PWD}/test/volumes/log/postgres-database.log";
			docker exec -i postgres psql -Uadmin -d itsm -c "\dt" > "${START_PWD}/test/volumes/log/postgres-tables.log";
			docker logs rabbitmq > "${START_PWD}/test/volumes/log/docker-log-rabbitmq.log";
			export exit_code=10;

		fi;
	else

		cd "${START_PWD}";

		if [ "0${GITHUB_SHA}"!="0" ]; then

			sudo chmod 777 -R "${START_PWD}/test"

		fi;

		echo 'Error: Failed to launch containers.';
		echo '';
		echo '';
		ls -lar "${START_PWD}/test";
		echo '';
		docker ps -a;
		docker logs centurion-erp-init > "${START_PWD}/test/volumes/log/docker-log-centurion-erp-init.log";
		docker logs centurion-erp> "${START_PWD}/test/volumes/log/docker-log-centurion-erp.log";
		docker logs postgres > "${START_PWD}/test/volumes/log/docker-log-postgres.log";
		docker exec -i postgres psql -Uadmin -c "\l" > "${START_PWD}/test/volumes/log/postgres-database.log";
		docker exec -i postgres psql -Uadmin -d itsm -c "\dt" > "${START_PWD}/test/volumes/log/postgres-tables.log";
		docker logs rabbitmq > "${START_PWD}/test/volumes/log/docker-log-rabbitmq.log";
		export exit_code=20;

	fi;

	if [ "0${GITHUB_SHA}"!="0" ]; then

		sudo chmod 777 -R "${START_PWD}/test"

	fi;

	echo '';
	docker ps -a;
	docker logs centurion-erp-init > "${START_PWD}/test/volumes/log/docker-log-centurion-erp-init.log";
	docker logs centurion-erp> "${START_PWD}/test/volumes/log/docker-log-centurion-erp.log";
	docker logs postgres > "${START_PWD}/test/volumes/log/docker-log-postgres.log";
	docker exec -i postgres psql -Uadmin -c "\l" > "${START_PWD}/test/volumes/log/postgres-database.log";
	docker exec -i postgres psql -Uadmin -d itsm -c "\dt" > "${START_PWD}/test/volumes/log/postgres-tables.log";
	docker logs rabbitmq > "${START_PWD}/test/volumes/log/docker-log-rabbitmq.log";
	export exit_code=0;
	cd "${START_PWD}/test";
	rm -f requirements_dev.txt;
	echo 'REmoving containers.';
	docker-compose down -v;
	cd "${START_PWD}";
	exit ${exit_code};



test-functional:
	pytest --cov-report xml:${PWD}/artifacts/coverage_functional.xml --cov-report html:${PWD}/artifacts/coverage/functional/ --junit-xml=${PWD}/artifacts/functional.JUnit.xml app/**/tests/functional


test-unit:
	pytest --cov-report xml:${PWD}/artifacts/coverage_unit.xml --cov-report html:${PWD}/artifacts/coverage/unit/ --junit-xml=${PWD}/artifacts/unit.JUnit.xml app/**/tests/unit



clean:
	rm -rf ${PATH_VENV}
	rm -rf artifacts
	rm -rf pages
	rm -rf build
	rm -rf node_modules
	rm -f package-lock.json
	rm -f package.json
	rm -rf .pytest_cache