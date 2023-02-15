#!/bin/bash

set -e

# Change directory to src
cd "${0%/*}"
cd ../src

# Build
npm run build
