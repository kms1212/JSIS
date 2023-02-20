#!/bin/bash

set -e

cd "${0%/*}"
cd ../src

rm -rf jsis.sqlite3*
find . -maxdepth 1 -mindepth 1 -type d -name '*api' -exec echo {} \; -exec rm -rf {}/migrations \; -exec mkdir -p {}/migrations \; -exec touch {}/migrations/__init__.py \;
