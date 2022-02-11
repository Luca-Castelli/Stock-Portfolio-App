#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db
python manage.py seed_users
python manage.py seed_stocks
python manage.py seed_fx
python manage.py seed_trade_log
python manage.py seed_stock_prices
python manage.py seed_fx_prices

exec "$@"