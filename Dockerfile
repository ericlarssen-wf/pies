# Get python dependencies as extra build step to hide credentials
# Start build stage
FROM python:3.6.4 as build

# Install node so we can use markdown-magic for README.md
RUN curl --silent --location https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g markdown-magic

ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL=https://pypi.python.org/simple/

COPY requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Download requirements so we can use them in our final stage
RUN pip download -r requirements.txt -d /build/dist

# Collect our dependencies for RM
ARG BUILD_ARTIFACTS_AUDIT=/audit/*
RUN mkdir /audit/
RUN pip freeze > /audit/pip.lock

# Build Environment Vars
WORKDIR /build/
COPY . /build/

# If this is a python package install
RUN pip install -qe .
# RUN pies --help

# End build stage

# Start check stage
FROM build as check
ENV CODECOV_TOKEN='bQ4MgjJ0G2Y73v8JNX6L7yMK9679nbYB'

WORKDIR /build/
ARG BUILD_ARTIFACTS_TEST_REPORTS=/build/test_results.xml
RUN make local-test

ARG BUILD_ARTIFACTS_PYPI=/build/dist/pies*.whl
RUN make local-package
RUN make local-codecov
# End check stage

# Start final container
FROM python:3.6

COPY --from=check /build/dist/* /dist/

EXPOSE 5000
RUN pip3 install $(find /dist -name \*.whl -or -name \*.tar.gz)
# End final container
