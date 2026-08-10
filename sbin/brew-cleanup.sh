#!/bin/sh
set -eu
brew="${HOME}/Utils/bin/brew.sh"
set -x
$brew autoremove
$brew cleanup --prune=all
