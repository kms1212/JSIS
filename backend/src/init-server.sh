#!/bin/bash

set -e

echo ===========================================
echo = 1. Network Connection Check
echo ===========================================
ifconfig
ping -c 3 database
ping -c 3 frontend


echo ===========================================
echo = 2. Migrate
echo ===========================================

app_lists=("authapi" "mainbbsapi" "fileapi" "communityapi" "classapi")

# check if migration archive exists
if ( cp /migrations/jsis.tar ./jsis.tar ); then
    mkdir migrations
    tar -xvf jsis.tar
    rm -rf jsis.tar
else
    mkdir migrations
fi

for app in ${app_lists[@]}; do
    mkdir -p "migrations/$app"
    mkdir -p "$app/migrations"
    
    # Copy file if any migration files exist
    if ls "migrations/$app/"* 1> /dev/null 2>&1; then
        mv "migrations/$app/"* "$app/migrations/"
    fi
done

for app in ${app_lists[@]}; do
    python manage.py makemigrations "$app"
done

python manage.py migrate

for app in ${app_lists[@]}; do
    cp "$app/migrations/"*.py "migrations/$app/"
done

tar -cvf jsis.tar migrations/*

cp jsis.tar /migrations/jsis.tar

python manage.py showmigrations


echo ===========================================
echo = 3. Run Server
echo ===========================================
gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker jsis.asgi:application
