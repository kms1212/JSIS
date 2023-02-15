#!/bin/bash

cd "${0%/*}"
cd ../src

pylint ./**/*.py --rcfile=../.pylintrc

exit 0
