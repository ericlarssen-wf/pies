#!/bin/bash
set -e

# Default to extracting an artifact named "dart_tool". This can be overriden
# by passing the name of a different artifact to the script.
artifact="${1:-dart_tool}"

files=$(find /build_artifacts/ -path "*/$artifact/*dart_tool.tgz")

count=${#files[@]}
if [ $count -ne 1 ]; then
    echo "Unable to find the dart tool build artifact"
    exit
fi

# Extract the .dart_tool tarball created in Workiva Build.
echo "tar xzf ${files[0]}"
tar xzf "${files[0]}"

# Extracting the .dart_tool (and pubspec.lock) isn't enough. We have to run
# `pub get` as well to generate the `.packages` file.
echo "pub get"
pub get
