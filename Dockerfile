# pull official base image
FROM python:slim as python-base
# docker build -t python-base --target python-base .

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base
# docker build -t poetry-base --target poetry-base .

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as app_image
# docker build -t app_image --target app_image .

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /usr/src/app

# Copy Dependencies
COPY poetry.lock pyproject.toml README.md ./

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
# RUN poetry install --no-interaction --no-cache --without dev
RUN poetry install --no-interaction --no-cache

# Copy Application
COPY ./src /usr/src/app


# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install system dependencies
# RUN apt update
# RUN apt upgrade
# RUN apt -y install gcc netcat-traditional
# # RUN apt -y install netcat
# RUN apt clean

# # copy requirements file
# COPY ./requirements.txt /usr/src/app/

# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # copy project
# COPY ./ /usr/src/app/
