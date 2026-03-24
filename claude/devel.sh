#!/bin/sh
set -eu
user=$(id -u -n)
exec docker run -it --rm -u "${user}" \
    --name "claude-devel" \
    --hostname claude-devel.debian.local \
    -e "TERM=${TERM}" \
    jrmsdev/claude
