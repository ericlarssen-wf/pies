#!/bin/sh
set -e

if [ ! -d ".dart_tool" ]; then
    exit
fi

echo "tar czf dart_tool.tgz"
tar czf dart_tool.tgz --exclude='*.snapshot' .dart_tool pubspec.lock
