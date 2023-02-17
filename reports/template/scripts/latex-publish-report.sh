#!/bin/bash

set -e

# Change directory to publish-report
cd "${0%/*}"
cd ../publish-report

# Build
xelatex report.tex

# Copy
DATE=$(date +%Y%m%dT%H%M%S)
cp report.pdf ../../report-$DATE.pdf
