#!/usr/bin/env bash

set -eu
set -x

# I think in future evolutions of this script, I would like to
# - orchestrate the service under test

# For now, you need to `./run.sh` in a separate terminal window

pact-verifier --provider-base-url=http://localhost:8082 ./pacts/*-farmer.json
