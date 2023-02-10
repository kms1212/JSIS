#!/bin/bash

set -e

####################################################################
### !!! This line will be replaced by the initializer script !!! ###
####################################################################

# Show logs of running container
RUNNING_CONTAINERS=$(sudo docker ps -q --filter ancestor=kms1212/jsis)

if [ -n "$RUNNING_CONTAINERS" ]; then
    sudo docker logs $RUNNING_CONTAINERS
fi
