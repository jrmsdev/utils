#!/bin/sh
set -eu
brew="${HOME}/Utils/bin/brew.sh"
bups="${HOME}/Backups/brew"
if test -d "${bups}.prev"; then
    rm -rf "${bups}.prev"
fi
if test -d "${bups}"; then
    mv -v "${bups}" "${bups}.prev"
fi
mkdir -vp "${bups}"
set -x
$brew config | tee "${bups}/brew.config"
$brew list --installed-on-request | tee "${bups}/brew.install"
$brew list --cask | tee -a "${bups}/brew.install"
$brew bundle dump --file "${bups}/Brewfile"
