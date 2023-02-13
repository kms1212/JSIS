#!/bin/bash

set -e

cd "${0%/*}"
cd ..

DOCKER_REGISTRY_HOST={{ docker_registry_host }}

echo "Building webapp..."

if [ "$1" != "-s" ]; then
    cd webapp
    npm run lint
    npm run build
    cd ..
fi


echo "Pushing to Docker Hub..."

docker buildx inspect xbuilder
if [ $? -ne 0 ]; then
    docker buildx create --name xbuilder
fi
docker buildx use xbuilder
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64 -t $DOCKER_REGISTRY_HOST/jsis-backend:latest --push jsis-docker
docker buildx build --platform linux/amd64 -t $DOCKER_REGISTRY_HOST/jsis-frontend:latest --push webapp-docker
