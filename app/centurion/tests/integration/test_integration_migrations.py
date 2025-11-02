import os
import pytest
import subprocess



class MigrationsTestCases:

    @pytest.fixture
    def run_command(self):

        def command(command: str):
            """
            Runs a specified shell command and returns (exit_code, stdout, stderr).
            """
            result = subprocess.run(
                command,
                shell=True,              # run through the shell
                capture_output=True,     # capture stdout and stderr
                text=True                # return strings instead of bytes
            )

            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }

        yield command



    @pytest.fixture( scope = 'function' )
    def truncate_database_sql_string(self, run_command):
        """
        Generates a SQL string to truncate all tables before each test,
        automatically detecting the DB backend.
        This string can be passed to `python manage.py dbshell`.
        """

        sql_statements = ""

        postgres = os.getenv('POSTGRES_IMAGE_TAG')
        mysql = os.getenv('MYSQL_IMAGE_TAG')
        if postgres is not None and postgres != "":
            backend = 'postgresql'
        elif mysql is not None and mysql != "":
            backend = 'mysql'
        else:
            backend = 'sqlite'




        backend = "postgresql"




        if backend == "postgresql":
            sql_statements = """
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN
                        SELECT tablename
                        FROM pg_tables
                        WHERE schemaname = 'public'
                    LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE;';
                    END LOOP;
                END $$;
            """

        elif backend in ("mysql", "mariadb"):
            sql_statements = """
                SET FOREIGN_KEY_CHECKS = 0;
                SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
                FROM information_schema.tables
                WHERE table_schema = DATABASE();
                SET FOREIGN_KEY_CHECKS = 1;
            """

        elif backend == "sqlite":
            sql_statements = """
                PRAGMA foreign_keys = OFF;
                SELECT 'DROP TABLE IF EXISTS "' || name || '";'
                FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%';
                PRAGMA foreign_keys = ON;
            """

        else:
            raise RuntimeError(f"Unsupported database backend: {backend}")

        cmd = 'docker exec -i centurion-erp ' + f'python manage.py dbshell <<\'EOF\'\n{sql_statements}\nEOF'

        print(cmd)

        result = run_command(
            cmd
        )

        print( result )

        if result['returncode']:
            raise Exception('Failed')


        yield



    @pytest.fixture(autouse=True, scope='function')
    def ensure_real_db(self):
        assert settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3' or \
            settings.DATABASES['default']['NAME'] != ':memory:', \
            "Tests are using in-memory SQLite, not your real DB"


    def test_run_migrations_fresh(self, truncate_database_sql_string, run_command):
        """Test Django Migrations

        Ensure that migrations run succussfully on a clean database.
        Equivilent command:

        - python manage.py
        """

        result = run_command('docker exec -i centurion-erp python manage.py migrate')

        print( result )

        assert result['returncode'] == 0, print(result)


    def test_run_migrations_upgrade(self, truncate_database_sql_string, run_command):
        """Test Django Migrations

        Ensure that migrations run succussfully when upgrading from the current release.
        Equivilent command:

        - Centurion Already deployed and matches current release v<latest-git-tag> (`git rev-list -n 1 $(git describe --tags --abbrev=0)`)
        - upgraded with:
            - python manage.py migrate
        """

        result = run_command("sh -c 'cd test; docker-compose rm -fs centurion; CENTURION_IMAGE_TAG=$(git rev-list -n 1 $(git describe --tags --abbrev=0)) \
docker-compose up -d centurion;'")

        print( result['stdout'] )

        assert result['returncode'] == 0, print( result )

        result = run_command('sh -c "sleep 30"')

        print( result )

        result = run_command('docker ps -a')

        print( result['stdout'] )

        result = run_command('docker exec -i centurion-erp python manage.py migrate')

        print( result['stdout'] )

        assert result['returncode'] == 0, print( result )

        result = run_command("sh -c 'cd test; docker-compose rm -fs centurion; CENTURION_IMAGE_TAG=$GITHUB_SHA \
docker-compose up -d centurion;'")

        print( result['stdout'] )

        assert result['returncode'] == 0, print( result )

        result = run_command('docker ps -a')

        print( result['stdout'] )

        result = run_command('docker exec -i centurion-erp python manage.py migrate')

        print( result['stdout'] )

        assert result['returncode'] == 0, print( result )



class MigrationsPyTest(
    MigrationsTestCases
):
    pass
