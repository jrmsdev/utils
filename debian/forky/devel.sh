#!/bin/sh
set -eu
user=$(id -u -n)
exec docker run -it --rm -u "${user}" \
    --name debian-forky \
    --hostname forky.debian.local \
    -e "TERM=${TERM}" \
    jrmsdev/debian-forky
