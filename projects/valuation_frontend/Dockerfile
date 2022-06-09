# https://nander.cc/using-selenium-within-a-docker-container
FROM python:3.9.13 as base
ARG AWS_ACCESS_KEY 
ARG AWS_SECRET_KEY 
ARG AWS_RDS_HOST 
ARG AWS_RDS_USER 
ARG AWS_RDS_PASSWORD 
ARG AWS_BUCKET_NAME 
ARG AWS_ACCOUNT_ID

ENV AWS_ACCESS_KEY=${AWS_ACCESS_KEY}
ENV AWS_SECRET_KEY=${AWS_SECRET_KEY}
ENV AWS_RDS_HOST=${AWS_RDS_HOST}
ENV AWS_RDS_USER=${AWS_RDS_USER}
ENV AWS_RDS_PASSWORD=${AWS_RDS_PASSWORD}
ENV AWS_BUCKET_NAME=${AWS_BUCKET_NAME}
ENV AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID}

FROM base as builder
ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN /env/bin/pip install --upgrade pip build wheel

COPY ./projects/library/common ./common
RUN python3 -m build ./common
RUN /env/bin/pip install ./common

COPY ./projects/valuation_frontend/requirements.txt ./
RUN /env/bin/pip install -r ./requirements.txt --no-deps

FROM builder as final
# Setup env
COPY --from=builder /env /env
COPY ./projects/valuation_frontend .

WORKDIR /valuation_frontend
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
