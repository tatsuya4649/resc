#!/bin/bash

DIR_DOCKER=$($(cd $(dirname $0)); pwd)
NAME=test_resc

# delete REMOTE HOST
echo "Delete Docker \"container\" and \"volume\"."
docker rm -f $(docker ps -aq --filter name=$NAME)
docker volume rm -f $(docker volume ls -q)
# delete Docker Image
echo "Delete Docker \"image\"."
if [ -n "$(docker images $NAME -q)" ]; then
    docker rmi -f $(docker images $NAME -q)
fi
