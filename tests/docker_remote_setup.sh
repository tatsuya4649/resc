#!/bin/bash

# $0 must be absolute path.
DIR_DOCKER="$(dirname $0)"
NAME=test_resc

# delete REMOTE HOST
if [ -n "$(docker ps -aq --filter name=$NAME)" ]; then
    docker rm -f $(docker ps -aq --filter name=$NAME)
fi
if [ -n "$(docker volume ls -q)" ]; then
    docker volume rm -f $(docker volume ls -q)
fi
# delete Docker Image
if [ -n "$(docker images $NAME -q)" ]; then
    echo "Delete Docker Image of \"$NAME\""
    docker rmi -f $(docker images $NAME -q)
fi
# build REMOTE HOST
echo "Build \"$NAME\" from Dockerfile."
docker build --tag $NAME $DIR_DOCKER
# run REMOTE HOST
echo "RUN \"$NAME\"."
docker run \
    --name $NAME \
    -p 20022:22 \
    -d \
    $NAME \

