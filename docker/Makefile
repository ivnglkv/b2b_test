dc=docker-compose
manage=docker-compose exec b2b_test-python python manage.py

migrations:
	$(manage) makemigrations

migrate:
	$(manage) migrate

build:
	$(dc) build

up:
	$(dc) up -d

dev: build up migrate

recreate:
	$(dc) stop
	make up
