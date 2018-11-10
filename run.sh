#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

### Active Waiting Loop

curl -sSf http://api-gateway:8080/
if [ $? -ne 0 ]; then
    echo -e " \n\n${RED}### API GATEWAY IS NOT AVAILABLE ! EXIT(1) ###${NC}\n"
    exit 1
fi

### Docker Compose 

echo -e " \n\n${GREEN}### Starting Behaviour Test Suite ###${NC}\n"

cd UberooBehaviour

docker-compose up --build --force-recreate
docker-compose down
