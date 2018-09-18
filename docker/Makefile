dc=docker-compose

migrate:
	$(dc) exec b2b_test-python python manage.py migrate

build:
	$(dc) build

up:
	$(dc) up -d

dev: build up migrate

recreate:
	$(dc) stop
	make up
