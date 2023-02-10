#!/bin/bash

set -e

####################################################################
### !!! This line will be replaced by the initializer script !!! ###
####################################################################

# Paths
MIGRATION_DIR=/migration
MEDIA_DIR=/media

LOCAL_MIGRATION_DIR=/data/migrations
LOCAL_MEDIA_DIR=/data/media

# Kill running containers
RUNNING_CONTAINERS=$(sudo docker ps -q --filter ancestor=kms1212/jsis)

if [ -n "$RUNNING_CONTAINERS" ]; then
    sudo docker kill  $RUNNING_CONTAINERS
fi

# Pull and run container
sudo docker pull kms1212/jsis
sudo docker run -v $LOCAL_MIGRATION_DIR:$MIGRATION_DIR -v $LOCAL_MEDIA_DIR:$MEDIA_DIR --add-host=host.docker.internal:host-gateway --env-file jsis.env -p 8000:8000 -p 8080:8080 -d kms1212/jsis:latest
sudo docker ps --filter ancestor=kms1212/jsis --format 'table {{.ID}}\t{{.Status}}\t{{.Names}}\t{{.Ports}}'
