.ONESHELL:

PATH_VENV := /tmp/centurion_erp

ACTIVATE_VENV :=. ${PATH_VENV}/bin/activate

START_PWD     := ${PWD}

.PHONY: clean prepare docs ansible-lint lint test

prepare-git-submodule:
	git submodule update --init;
	git submodule foreach git submodule update --init;


prepare-python: prepare-git-submodule
	python3 -m venv ${PATH_VENV};
	${ACTIVATE_VENV};
	pip install -r website-template/gitlab-ci/mkdocs/requirements.txt;
	pip install -r gitlab-ci/lint/requirements.txt;
	pip install -r gitlab-ci/mkdocs/requirements.txt;
	pip install -r requirements.txt;
	pip install -r requirements_dev.txt;

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

			echo 'Stoping Gunicorn.';
			docker exec -i centurion-erp supervisorctl stop gunicorn;
			echo 'Cleaning artifacts dir.';
			docker exec -i centurion-erp sh -c 'rm -rf /app/artifacts/* /app/artifacts/.[!.]*';
			echo 'Starting Gunicorn.';
			docker exec -i centurion-erp supervisorctl start gunicorn;
			sleep 60;
			docker ps -a;
			curl --trace-ascii - http://localhost:8003/api;
			echo '--------------------------------------------------------------------';
			curl --trace-ascii - http://127.0.0.1:8003/api;


			docker logs centurion-erp;
			echo 'Starting integration tests.';
			pytest --override-ini addopts= --no-migrations --reuse-db --tb=long --verbosity=2 --showlocals --junit-xml="${START_PWD}/integration.JUnit.xml" app/*/tests/integration;
			echo 'Restarting Gunicorn.';
			docker exec -i centurion-erp supervisorctl restart gunicorn;
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