from python:3.6

copy . /home/app
workdir /home/app
cmd pip install requirements.txt

EXPOSE 8050

cmd /home/app/start.sh

