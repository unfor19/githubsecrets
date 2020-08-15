FROM python:3.8.5-slim as build
RUN python -m pip install wheel==0.34.2 setuptools==44.1.0 twine==3.1.1 docutils>=0.16
WORKDIR /code
COPY . .
RUN python -m venv ./ENV \
    && . ./ENV/bin/activate \
    && python -m pip install --no-cache-dir --upgrade pip keyrings.alt  \
    && python -m pip install --no-cache-dir --editable . \
    && chmod +x /code/entrypoint.sh

FROM python:3.8.5-slim as app
WORKDIR /code
COPY --from=build /code /code/
ENTRYPOINT ["/code/entrypoint.sh"]
