

# Run project

```docker compose up```

# Migrations
```
docker compose -f docker-compose.yaml run --rm web python manage.py makemigrations
```
```
docker compose -f docker-compose.yaml run --rm web python manage.py migrate
```
```
docker compose -f docker-compose.yaml run --rm web python manage.py createsuperuser
```