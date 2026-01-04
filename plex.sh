#!/bin/bash

sudo docker stop plex

sudo docker pull plexinc/pms-docker

sudo docker rm plex

sudo docker run \
-d \
--name plex \
--restart always \
--network=host \
-e TZ="America/Toronto" \
-e PLEX_CLAIM="<TOKEN>" \
-v /home/ryan/plex/config:/config \
-v /home/ryan/plex/transcode:/transcode \
-v /mnt/pool/Media:/data \
plexinc/pms-docker:latest
