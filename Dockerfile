FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip
#RUN #wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
RUN unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
RUN mv /usr/local/bin/chromedriver-linux64 /usr/local/bin/chromedriver

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install -r /code/requirements.txt

CMD ["python", "-u", "/code/main.py"]