# Get python dependencies as extra build step to hide credentials
# Start build stage
FROM python:2.7 as build

ARG GIT_SSH_KEY
ARG KNOWN_HOSTS_CONTENT

RUN mkdir /root/.ssh
RUN echo "$KNOWN_HOSTS_CONTENT" > "/root/.ssh/known_hosts"
RUN chmod 700 /root/.ssh/
RUN umask 0077 && echo "$GIT_SSH_KEY" >/root/.ssh/id_rsa
RUN eval "$(ssh-agent -s)" && ssh-add /root/.ssh/id_rsa

# Install node so we can use markdown-magic for README.md
RUN curl --silent --location https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g markdown-magic

ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL=https://pypi.python.org/simple/

RUN pip install pip==9.0.3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip download -r requirements.txt -d /build/dist

WORKDIR /build/
COPY . /build/

# If this is a python package install
RUN pip install -e .

FROM build as check
WORKDIR /build/

ARG BUILD_ARTIFACTS_PYPI=/build/dist/pies*.whl
RUN make local-package

FROM python:2.7

COPY --from=check /build/dist/* /dist/
EXPOSE 5000

RUN pip install pip==9.0.3
RUN pip install --no-index --find-links=/dist $(find /dist -name \*.whl -or -name \*.tar.gz)
ADD config.py /config.py
# End final container
