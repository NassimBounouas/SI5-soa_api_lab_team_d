#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

####

echo -e " \n\n${RED}### Starting Behaviour Test Suite ###${NC}\n"

cd UberooBehaviour

docker-compose up --force-recreate
docker-compose down
