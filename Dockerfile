FROM python:3.6

COPY . /home/app
WORKDIR /home/app

RUN python -m venv env && \
    ./env/bin/pip install -r requirements.txt && \
    chmod +x start.sh

CMD ./env/bin/python ./env/bin/gunicorn -w 4 -b 0.0.0.0:8080 app:app

