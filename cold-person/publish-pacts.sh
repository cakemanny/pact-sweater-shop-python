#!/bin/sh

set -eu
set -x

cd "$(dirname "$0")"

mkdir -p ../knitter/pacts/.
cp -r pacts/*.json ../knitter/pacts/.
mkdir -p ../hatter/pacts/.
cp -r pacts/*.json ../hatter/pacts/.
