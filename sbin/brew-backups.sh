#!/bin/sh
set -eu
brew="${HOME}/Utils/bin/brew.sh"
bups="${HOME}/Backups/brew"
mkdir -vp "${bups}"
set -x
$brew config | tee "${bups}/brew.config"
$brew list --installed-on-request | tee "${bups}/brew.install"
$brew list --cask | tee -a "${bups}/brew.install"
