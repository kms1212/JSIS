#!/bin/bash

set -e

# Change directory to src
cd "${0%/*}"
cd ../src

# Build
npx tailwindcss -i tailwind.scss -o ./src/assets/css/tailwind.css
npm run build
