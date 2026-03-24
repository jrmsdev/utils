#!/bin/bash
set -eu

user=$(id -u -n)

workspace="${HOME}/Workspace"
github="${HOME}/Github"
temp="${HOME}/Temp"

install -v -d -m 0750 "${workspace}"
install -v -d -m 0750 "${github}"
install -v -d -m 0750 "${temp}"

datadir="${HOME}/Docker/claude"
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
	-v "${workspace}:/home/${user}/workspace" \
	-v "${github}:/home/${user}/github" \
	-v "${temp}:/home/${user}/temp" \
	--workdir "/home/${user}" \
	jcroots/claude
