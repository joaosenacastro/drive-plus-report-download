FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/

RUN apt -y update
RUN apt install -y chromium chromium-driver

RUN apt-get install -y xvfb
# set display port to avoid crash
ENV DISPLAY=:99

RUN pip3 install pyvirtualdisplay

RUN pip install -r /code/requirements.txt

CMD ["python", "-u", "/code/main.py"]