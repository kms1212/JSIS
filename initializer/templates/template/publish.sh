#!/bin/bash

set -e

####################################################################
### !!! This line will be replaced by the initializer script !!! ###
####################################################################

cd "${0%/*}"

# Default values
BUILD_TYPE="SNAPSHOT"
BUILD_VERSION=""
SKIP_WEBAPP_BUILD="false"

while getopts "hst:v:" opt
do
        case $opt in
                h) echo "Usage: $0 [-h] [-t BUILD_TYPE] [-v BUILD_VERSION]"
                   echo "  -h: Show this help message."
                   echo "  -s: Skip build."
                   echo "  -t: Build type. (RELEASE, BETA, SNAPSHOT)"
                   echo "  -v: Build version. (Required for RELEASE and BETA build)"
                   exit 0;;
                s) SKIP_WEBAPP_BUILD="true";;
                t) BUILD_TYPE="$OPTARG";;
                v) BUILD_VERSION="$OPTARG";;
                *) echo "Invalid argument: $opt"; exit 1;;
        esac
done

if [ "$BUILD_TYPE" = "RELEASE" ]; then
    if [ -z "$BUILD_VERSION" ]; then
        echo "BUILD_VERSION is required for release build."
        exit 1
    fi
elif [ "$BUILD_TYPE" = "BETA" ]; then
    if [ -z "$BUILD_VERSION" ]; then
        echo "BUILD_VERSION is required for beta build."
        exit 1
    fi
elif [ "$BUILD_TYPE" = "SNAPSHOT" ]; then
    BUILD_VERSION="SNAPSHOT-$(date +%Y%m%d%H%M%S)"
else
    echo "Invalid BUILD_TYPE: $BUILD_TYPE"
    exit 1
fi


####################################################################
echo "Building webapp..."

if [ "$SKIP_WEBAPP_BUILD" = "false" ]; then
    cd webapp
    npm run lint
    npm run build
    cd ..
fi

####################################################################
echo "Pushing to Docker Hub..."

docker buildx inspect xbuilder
if [ $? -ne 0 ]; then
    docker buildx create --name xbuilder
fi
docker buildx use xbuilder
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64 -t kms1212/jsis:$BUILD_VERSION -t kms1212/jsis:latest --push . 
