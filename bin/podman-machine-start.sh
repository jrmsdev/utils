#!/bin/bash
/opt/homebrew/bin/podman machine stop
exec /opt/homebrew/bin/podman machine start --quiet --no-info
