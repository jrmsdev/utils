#!/bin/sh
set -eu

_USER=$(id -u -n)
_UID=$(id -u)
_GID=$(id -g)

exec docker build --rm \
    --build-arg "USER_NAME=${_USER}" \
    --build-arg "USER_UID=${_UID}" \
    --build-arg "USER_GID=${_GID}" \
    -t jrmsdev/debian-forky .
