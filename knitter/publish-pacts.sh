#!/bin/sh

set -eu
set -x

mkdir -p ../farmer/pacts/.
cp -r pacts/knitter-farmer.json ../farmer/pacts/.
