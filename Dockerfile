### --------------------------------------------------------------------
### Docker Build Arguments
### Available only during Docker build - `docker build --build-arg ...`
### --------------------------------------------------------------------
ARG PYTHON_VERSION="3.9.0"
ARG APP_NAME="githubsecrets"
ARG APP_ARTIFACT_DIR="artifact/"
ARG APP_HOME_DIR="/app"
ARG APP_USER_NAME="appuser"
ARG APP_GROUP_ID="appgroup"
### --------------------------------------------------------------------


### --------------------------------------------------------------------
### Build Stage
### --------------------------------------------------------------------
FROM python:$PYTHON_VERSION-slim as build

# Define env vars
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Define workdir
WORKDIR /code/

# Upgrade pip and then install build tools
RUN pip install --upgrade pip && \
    pip install --upgrade wheel setuptools wheel check-wheel-contents

# Copy the application from Docker build context to WORKDIR
COPY . .

# Build the application and validate wheel contents
RUN python setup.py bdist_wheel && \
    find dist/ -type f -name *.whl -exec check-wheel-contents {} \;

# For debugging the Build Stage
CMD ["bash"]
### --------------------------------------------------------------------


### --------------------------------------------------------------------
### App Stage
### --------------------------------------------------------------------
FROM python:$PYTHON_VERSION-slim as app

# Fetch values from ARGs that were declared at the top of this file
ARG APP_NAME
ARG APP_ARTIFACT_DIR
ARG APP_HOME_DIR
ARG APP_USER_NAME
ARG APP_GROUP_ID

# Define workdir
ENV HOME="${APP_HOME_DIR}"
WORKDIR "${HOME}"

# Define env vars
ENV APP_NAME="${APP_NAME}"
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PATH="${HOME}/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y libdbus-glib-1-dev gcc

# Run as a non-root user
RUN addgroup "${APP_GROUP_ID}" && \
    useradd "${APP_USER_NAME}" --gid "${APP_GROUP_ID}" --home-dir "${HOME}" && \
    mkdir "${APP_ARTIFACT_DIR}" && \
    chown -R ${APP_USER_NAME} .
USER "${APP_USER_NAME}"

# Upgrade pip, setuptools and wheel
RUN pip install --user --upgrade pip && \
    pip install --user --upgrade setuptools wheel keyrings.alt

# Copy requirements.txt from Build Stage
COPY --from=build /code/requirements.txt "${APP_ARTIFACT_DIR}"

# Install requirements
RUN pip install --user -r "${APP_ARTIFACT_DIR}/requirements.txt"

# Copy artifacts from Build Stage
COPY --from=build /code/dist/ "${APP_ARTIFACT_DIR}"

# Install the application from local wheel package
RUN find . -type f -name *.whl -exec pip install --user {} \; -exec rm {} \;  && \
    rm -r "${APP_ARTIFACT_DIR}"

# The container runs the application, or any other supplied command, such as "bash" or "echo hello"
# CMD python -m ${APP_NAME}

# Use ENTRYPOINT instead CMD to force the container to start the application
ENTRYPOINT ["ghs"]
### --------------------------------------------------------------------