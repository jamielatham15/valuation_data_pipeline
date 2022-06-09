# https://nander.cc/using-selenium-within-a-docker-container
FROM python:3.9.13 as base

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
