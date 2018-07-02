FROM python:3.6

COPY . /home/app
WORKDIR /home/app

RUN python -m venv env && \
    ./env/bin/pip install -r requirements.txt && \
    chmod +x start.sh

EXPOSE 8080

CMD ./env/bin/python app.py

