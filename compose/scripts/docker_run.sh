#!/bin/bash

set -e

cd "${0%/*}"

sudo docker compose pull
sudo docker compose up -d
