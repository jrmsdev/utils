#!/bin/bash
set -eux
cd "${HOME}/Github/jcroots/dockerfiles"
make debian
make brew
make claude
