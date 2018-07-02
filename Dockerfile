FROM python:3.6

COPY . /home/app
WORKDIR /home/app
RUN python -m venv env && \
    ./env/bin/pip install -r requirements.txt

EXPOSE 8050

CMD /home/app/start.sh

