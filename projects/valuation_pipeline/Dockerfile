# https://nander.cc/using-selenium-within-a-docker-container
FROM python:3.9.13 as base
ARG AWS_ACCESS_KEY 
ARG AWS_SECRET_KEY 
ARG AWS_RDS_HOST 
ARG AWS_RDS_USER 
ARG AWS_RDS_PASSWORD 
ARG AWS_BUCKET_NAME 
ARG AWS_ACCOUNT_ID 
ARG DATA_HOST 
ARG DATA_USER 
ARG DATA_PASSWORD

ENV AWS_ACCESS_KEY=$AWS_ACCESS_KEY
ENV AWS_SECRET_KEY=$AWS_SECRET_KEY
ENV AWS_RDS_HOST=$AWS_RDS_HOST
ENV AWS_RDS_USER=$AWS_RDS_USER
ENV AWS_RDS_PASSWORD=$AWS_RDS_PASSWORD
ENV AWS_BUCKET_NAME=$AWS_BUCKET_NAME
ENV AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID
ENV DATA_HOST=$DATA_HOST
ENV DATA_USER=$DATA_USER
ENV DATA_PASSWORD=$DATA_PASSWORD

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
RUN true
COPY ./projects/valuation_pipeline/valuation_pipeline /app

WORKDIR /app
CMD ["python3", "runner.py"]