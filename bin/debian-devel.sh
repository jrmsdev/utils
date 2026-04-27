#!/bin/bash
set -eu

user=$(id -u -n)

temp="${HOME}/Temp"
install -v -d -m 0750 "${temp}"

exec docker run -it --rm -u "${user}" \
	--hostname debdev.debian.local \
	-e "TERM=${TERM}" \
	-v "${temp}:/home/${user}/temp" \
	--workdir "/home/${user}" \
	jrmsdev/debian-devel
