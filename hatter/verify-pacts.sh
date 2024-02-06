#!/usr/bin/env bash

set -eu
set -x

# You need to `PACT_VERIFICATION=true ./run.sh` in a separate terminal window

pact-verifier --provider-base-url=http://localhost:8083 \
    --provider-states-setup-url=http://localhost:8083/_/pact/provider-states \
    ./pacts/coldperson-hatter.json
