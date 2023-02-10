#!/bin/bash

set -e

####################################################################
### !!! This line will be replaced by the initializer script !!! ###
####################################################################

# Execute bash in running container
RUNNING_CONTAINERS=$(sudo docker ps -q --filter ancestor=kms1212/jsis)

if [ -n "$RUNNING_CONTAINERS" ]; then
    sudo docker exec -it $RUNNING_CONTAINERS /bin/bash
fi
