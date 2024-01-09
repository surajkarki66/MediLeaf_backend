.PHONY: install
install:
	pip install -r "requirements.txt"

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate;python manage.py loaddata --app account initial_data;python manage.py loaddata --app plant initial_data

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: run
run:
	python manage.py runserver