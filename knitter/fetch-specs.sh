#!/usr/bin/env bash

set -eu
set -x

# Update our copy of the farmer spec
# Needs the farmer service to be running

curl --fail 'http://localhost:8082/openapi.json' -o specs/Farmer-openapi.json
