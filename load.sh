#!/bin/bash
# @author: Nassim BOUNOUAS
# @author: Nikita ROUSSEAU
# @date: 10/11/2018

### Colors

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

### Current Working Directory

cwd=$(pwd)

### API Gateway Active Waiting Loop

echo -e " \n\n${BLUE}### Testing API Gateway availability... ###${NC}\n"

curl -sSf http://127.0.0.1:8080/status > /dev/null

if [ $? -ne 0 ]; then
    echo -e " \n\n${RED}### API GATEWAY IS NOT AVAILABLE ! EXIT(1) ###${NC}\n"
    exit 1
fi

### Load Runner

echo -e " \n\n${GREEN}### Launching Load Runner... ###${NC}\n"
cd UberooLoadRunner

docker-compose up --build --force-recreate

### Clean up

echo -e " \n\n${ORANGE}### Clean up... ###${NC}\n"
docker-compose down

cd $cwd