#!/bin/sh
set -eu
user=$(id -u -n)
exec docker run -it --rm -u "${user}" \
    --name debian-devel \
    --hostname debdev.debian.local \
    -e "TERM=${TERM}" \
    jrmsdev/debian-devel
