#!/bin/sh

set -e

echo "Installing python test requirements......";
docker exec -i centurion-erp pip install -r /requirements_test.txt;
echo "Complete: Installing python test requirements.";

echo "Restarting Gunicorn";
docker exec -i centurion-erp supervisorctl restart gunicorn;
echo "Complete: Restarting Gunicorn";


CONTAINER_NAME="centurion-erp-init"
TIMEOUT=400
INTERVAL=5
ELAPSED=0
STATUS=""

while [ "$STATUS" != "exited" ] && [ "$STATUS" != "dead" ]; do

  STATUS=$(docker inspect --format '{{.State.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "not_found")


  if [ "$STATUS" = "not_found" ]; then
    docker ps -a
    echo "Container $CONTAINER_NAME was not found."
    exit 2
  fi

  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout reached. Container $CONTAINER_NAME still running (status: $STATUS)."
    exit 3
  fi

  echo "Waiting for container $CONTAINER_NAME to complete... Current status: $STATUS"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "Container $CONTAINER_NAME has completed."


CONTAINER_NAME="centurion-erp"
TIMEOUT=90
INTERVAL=5
ELAPSED=0
STATUS=""

while [ "$STATUS" != "healthy" ]; do
  STATUS=$(docker inspect --format '{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "none")

  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout reached. Container $CONTAINER_NAME is not healthy."
    exit 4
  fi

  echo "Waiting for container $CONTAINER_NAME to be healthy... Current status: $STATUS"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

#
# migrated to test suite fixture
#
# echo "Creating centurion super user.";
# docker exec -i centurion-erp python manage.py createsuperuser --username admin --email admin@localhost --noinput

# echo "Installing application expect.";
# docker exec -i centurion-erp apk add expect

# echo "Setting super user password.";
# docker exec -i centurion-erp expect -c "
#     spawn python manage.py changepassword admin
#     expect \"Password:\"
#     send \"admin\r\"
#     expect \"Password (again):\"
#     send \"admin\r\"
#     expect eof
# "
