#!/usr/bin/env bash

set -eu
set -x

# I think in future evolutions of this script, I would like to
# - spawn a stub server to play Farmer
# - orchestrate the service under test
# some ideas in : https://medium.com/swlh/the-ultimate-guide-to-integration-testing-with-docker-compose-and-sql-f288f05032c9
#  and  docker compose up --exit-code-from test-service-name  is also an idea

# For now, you need to `knitter-serve` in a separate terminal window
# and also in another, the stub server:
#   docker run -it --rm -p 8082:8082 -v "$PWD/pacts/:/app/pacts" pactfoundation/pact-stub-server -p 8082 -d pacts
#

pact-verifier --provider-base-url=http://localhost:8081 ./pacts/coldperson-knitter.json
