FROM google/dart:2.7.2 as build
RUN dart --version

# Don't allow the dart package to be updated via apt
RUN apt-mark hold dart

# Update image, install deps
RUN apt-get update -qq && \
    apt-get dist-upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all
RUN apt-get install -y \
	build-essential \
	curl \
	git \
	make \
	parallel \
	wget \
	&& rm -rf /var/lib/apt/lists/*

# Activate global libraries
RUN pub global activate webdev ^2.0.0
RUN pub global activate coverage

# For convenience, add the Dart package cache to the user's PATH
ENV PATH=$PATH:/root/.pub-cache/bin

# These allow the Dart VM to access 32GB of memory on Linux if needed.
# BUILD_DART2JS_VM_ARGS is needed to get the flag used when webdev or
# build_runner spawn dart subprocesses.
ENV DART_VM_OPTIONS="--old-gen-heap-size=32000"
ENV BUILD_DART2JS_VM_ARGS="--old-gen-heap-size=32000"

# Install utility scripts
COPY scripts/* /usr/local/bin/
WORKDIR /build/
ADD pubspec.yaml /build/
RUN pub get
FROM scratch
