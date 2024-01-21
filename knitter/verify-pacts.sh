#!/usr/bin/env bash

set -eu
set -x

# I think in future evolutions of this script, I would like to
# - spawn a stub server to play Farmer
# - orchestrate the service under test

# For now, you need to `knitter-serve` in a separate terminal window

pact-verifier --provider-base-url=http://localhost:8081 --pact-url=./pacts/coldperson-knitter.json
