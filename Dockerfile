FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 8000 2222
# TODO: research how to pass the api key securely :)
CMD gunicorn --bind=0.0.0.0 --timeout 600 --env API_KEY=03X1PDdf3nTualFvT5V6owA7P8lPsRsD app:app
