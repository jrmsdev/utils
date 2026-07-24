#!/bin/bash
set -eu
cd ~/Github/jrmsdev/jobsearch
open -a 'Brave Browser' -n --args \
  --new-instance \
  --incognito \
  http://127.0.0.1:8046/
exec ./docker/run.sh
