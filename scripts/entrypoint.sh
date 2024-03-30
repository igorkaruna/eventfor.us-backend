#!/bin/bash


wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        echo "PostgreSQL is not up yet..."
        sleep 1
    done
}


manage_command() {
    echo "Running command: python src/manage.py $*"
    if ! python src/manage.py "$@"; then
        echo "Command '$*' failed. Exiting..."
        exit 1
    fi
}


wait_for_postgres


if [[ "$RUN_MIGRATIONS" == "1" ]]; then
    echo "Checking for database migrations..."
    manage_command migrate
fi

if [[ "$COLLECT_STATIC" == "1" ]]; then
    echo "Collecting static files..."
    manage_command collectstatic --noinput
fi


echo "Executing command: $*"
exec "$@"
