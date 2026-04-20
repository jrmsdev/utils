#!/bin/sh
set -eu
brew="${HOME}/Utils/bin/brew.sh"
set -x
$brew update
$brew outdated --greedy
