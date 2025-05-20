# variables
COMPOSE = sudo docker compose
APP_NAME = web  # name of the service in the docker-compose.yml

# docker commands
up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down && $(COMPOSE) up --build

logs:
	$(COMPOSE) logs -f

# django commands
migrate:
	$(COMPOSE) exec $(APP_NAME) python manage.py migrate

makemigrations:
	$(COMPOSE) exec $(APP_NAME) python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec $(APP_NAME) python manage.py createsuperuser

create_fake_data:
	$(COMPOSE) exec $(APP_NAME) python manage.py create_fake_data

shell:
	$(COMPOSE) exec $(APP_NAME) python manage.py shell

shell_plus:
	$(COMPOSE) exec $(APP_NAME) python manage.py shell_plus

bash:
	$(COMPOSE) exec $(APP_NAME) /bin/bash

run:
	$(COMPOSE) exec $(APP_NAME) python manage.py runserver 0.0.0.0:8000

test:
	$(COMPOSE) exec $(APP_NAME) python manage.py test

runscript:
	$(COMPOSE) exec $(APP_NAME) python manage.py runscript script

# utils
collectstatic:
	$(COMPOSE) exec $(APP_NAME) python manage.py collectstatic --noinput

check:
	$(COMPOSE) exec $(APP_NAME) python manage.py check

# elastic search
create:
	$(COMPOSE) exec $(APP_NAME) python manage.py search_index --create

populate:
	$(COMPOSE) exec $(APP_NAME) python manage.py search_index --populate

rebuild:
	$(COMPOSE) exec $(APP_NAME) python manage.py search_index --rebuild


# postgres
drop_db:
	$(COMPOSE) exec db psql -U $$POSTGRES_USER -d postgres -c "DROP DATABASE 'django_db';"
