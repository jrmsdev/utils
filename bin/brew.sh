#!/bin/sh
umask 0022
exec /opt/homebrew/bin/brew "$@"
