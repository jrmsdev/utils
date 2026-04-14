#!/bin/bash
set -eu
exec open -a 'Brave Browser' -n --args \
  --new-instance \
  --incognito
