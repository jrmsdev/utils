#!/bin/bash
set -eu

user=$(id -u -n)

github="${HOME}/Github"
temp="${HOME}/Temp"
utils="${HOME}/Utils"

install -v -d -m 0750 "${github}"
install -v -d -m 0750 "${temp}"
install -v -d -m 0750 "${utils}"

datadir="${HOME}/Docker/claude"
install -v -d -m 0750 "${HOME}/Docker"
install -v -d -m 0750 "${datadir}"
install -v -d -m 0750 "${datadir}/config"

if ! test -s "${datadir}/claude.json"; then
	touch "${datadir}/claude.json"
fi

exec docker run -it --rm -u "${user}" \
	--hostname "claude.debian.local" \
	-e "TERM=${TERM}" \
	-v "${datadir}/config:/home/${user}/.claude" \
	-v "${datadir}/claude.json:/home/${user}/.claude.json" \
	-v "${github}:/home/${user}/github:ro" \
	-v "${utils}:/home/${user}/utils" \
	-v "${temp}:/home/${user}/temp" \
	--workdir "/home/${user}" \
	jrmsdev/claude
