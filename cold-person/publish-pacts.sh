#!/bin/sh

set -eu
set -x

mkdir -p ../knitter/pacts/.
cp -r pacts/*.json ../knitter/pacts/.
