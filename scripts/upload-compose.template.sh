#!/bin/bash

set -e

cd "${0%/*}"

SSH_HOST={{ ssh_host }}
SSH_USER={{ ssh_user }}
REMOTE_DIR={{ remote_dir }}

scp ../compose/* $SSH_USER@$SSH_HOST:$REMOTE_DIR