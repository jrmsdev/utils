#!/bin/sh
set -eu
brew="${HOME}/Utils/bin/brew.sh"
brew_cleanup="${HOME}/Utils/sbin/brew-cleanup.sh"
set -x
$brew update
$brew outdated --greedy
$brew upgrade --greedy --yes
$brew_cleanup
