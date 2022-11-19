release: python manage.py migrate
web: daphne market_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=market_project.settings -v2
