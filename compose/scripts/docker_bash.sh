#!/bin/bash

set -e

cd "${0%/*}"

sudo docker compose exec $1 bash
