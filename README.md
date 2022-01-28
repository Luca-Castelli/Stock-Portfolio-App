docker-compose exec server python manage.py create_db
docker-compose exec server python manage.py seed_db
docker-compose exec db psql --username=luca --dbname=dev

docker system prune -a
