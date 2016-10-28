help:
	@echo "Here are available targets:"
	@egrep -o "^#: (.+)" [Mm]akefile  | sed 's/#: /* /'


#: install - Setup developmnet enviroment.
install: python-requirements upgrade-migrations runserver


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
