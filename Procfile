    web: python manage.py createcachetable && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn drnalpha.wsgi:application --bind 0.0.0.0:$PORT -c gunicorn-conf.py --workers 3 --max-requests 1200 --max-requests-jitter 50 --access-logfile -
