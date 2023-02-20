#!/bin/bash

set -e

cd "${0%/*}"
cd ../src

python manage.py makemigrations --settings=jsis.settings_test
python manage.py migrate --settings=jsis.settings_test