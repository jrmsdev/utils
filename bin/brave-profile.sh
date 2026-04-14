#!/bin/bash
set -eu
NAME=${1:?'profile name?'}
exec open -a 'Brave Browser' -n --args \
  --user-data-dir="${HOME}/Library/Application Support/BraveProfiles/${NAME}" \
  --new-instance
