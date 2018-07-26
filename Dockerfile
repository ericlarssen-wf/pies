FROM python:3.6

ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL=https://pypi.python.org/simple/
ARG GIT_BRANCH
ARG GIT_COMMIT

# ARG GIT_SSH_KEY
# ARG KNOWN_HOSTS_CONTENT
#
# RUN mkdir /root/.ssh
# RUN echo "$KNOWN_HOSTS_CONTENT" > "/root/.ssh/known_hosts"
# RUN chmod 700 /root/.ssh/
# RUN umask 0077 && echo "$GIT_SSH_KEY" >/root/.ssh/id_rsa
# RUN eval "$(ssh-agent -s)" && ssh-add /root/.ssh/id_rsa

WORKDIR /build/
COPY . /build/

RUN pip install pip==9.0.3
RUN echo "installing requirements" && \
		pip install -e . && \
    echo "done"

RUN python setup.py sdist

ENTRYPOINT ["python"]
CMD ["pies/main.py"]
