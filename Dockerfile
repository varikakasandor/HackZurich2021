FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip nginx && \
    pip3 install uwsgi

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
COPY ./nginx.conf /etc/nginx/sites-enabled/default

# ENTRYPOINT [ "python" ]

# CMD [ "app.py" ]
CMD gunicorn --bind=0.0.0.0 --timeout 600 app:app
# CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:app
