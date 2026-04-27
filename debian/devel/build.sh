#!/bin/sh
set -eu
_USER=$(id -u -n)
exec docker build --rm \
	--build-arg "USER_NAME=${_USER}" \
	-t jrmsdev/debian-devel .
