#!/bin/bash
curl -sSf http://127.0.0.1:8080/ 2> /dev/null

if [ $? -eq 0 ]; then
    echo -e " \n\n${RED}### LOCALHOST PORT 8080 IS ALREADY BOUND ! PLEASE RELEASE THE PORT ! ###${NC}\n"
    exit 1
fi
    echo -e " \n\n${GREEN}### LOCALHOST PORT 8080 IS FREE ! WE CAN CONTINUE ! ###${NC}\n"
