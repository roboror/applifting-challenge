#!/bin/bash
set +xe

docker-compose build productaggregator
docker-compose run productaggregator pytest  --cov=. -s
