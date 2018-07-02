from python:3.6

copy . /app
workdir /app
cmd pip install requirements.txt

EXPOSE 8050

cmd /app/start.sh

