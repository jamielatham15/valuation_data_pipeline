# https://nander.cc/using-selenium-within-a-docker-container
FROM python:3.9.13 as base

# Setup chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install chrome driver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

FROM base as builder
ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN /env/bin/pip install --upgrade pip build wheel

COPY ./projects/library/common ./common
RUN python3 -m build ./common
RUN /env/bin/pip install ./common

COPY ./projects/valuation_pipeline/requirements.txt ./
RUN /env/bin/pip install -r ./requirements.txt --no-deps

FROM builder as final
# Setup env
COPY --from=builder /env /env
COPY ./projects/valuation_pipeline/ .


