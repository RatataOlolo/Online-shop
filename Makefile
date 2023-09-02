up:
	docker-compose -f docker-compose.yml up $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up $(c)

build:
	docker-compose build

logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)

migrate:
	docker-compose run python python manage.py migrate

postgres:
	docker-compose -f docker-compose.yml exec postgres psql -Upostgres

bash:
	docker-compose -f docker-compose.yml exec python /bin/bash

superuser:
	docker-compose run python python manage.py createsuperuser