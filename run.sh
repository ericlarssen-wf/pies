#!/bin/bash

function log {
while [ 1 ]   # Endless loop.
do
  sleep 5
  echo "Here I go breaking again!"
  exit
done
}

log &

/usr/sbin/nginx
