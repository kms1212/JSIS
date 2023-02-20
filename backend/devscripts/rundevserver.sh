#!/bin/bash

set -e

cd "${0%/*}"
cd ../src

python manage.py runserver --settings=jsis.settings_test