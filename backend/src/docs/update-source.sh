#!/bin/bash

set -e

cd "${0%/*}"

sphinx-apidoc -f -o source ../ ../**/migrations/