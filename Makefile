help:
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: install - Setup developmnet enviroment.
install: python-requirements upgrade-migrations


#: docker-install - Setup developmnet enviroment with Docker
docker-install: docker-build docker-run


#: test - Run the test suite and outputs a coverage report.
test:
	py.test -sv --cov


#: runserver - Start the adapted development server.
runserver:
	python manage.py runserver


python-requirements:
	pip install -r requirements.txt


upgrade-migrations:
	python manage.py db upgrade


docker-build:
	docker build -t messaging-thiago-costa:latest .


docker-run:
	docker run -d -p 5000:5000 messaging-thiago-costa
