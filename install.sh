#!/bin/bash
echo -e "Eta_Computer, Ordering and Menu Services are in Python - they don't need to be compiled\n\n"

echo -e "Building Chinese_Restaurant and Delivery Services - Go must be installed on your system\n"
cd Chinese_Restaurant_Service/Service
./build.sh
cd ../../Delivery_Service/Service
./build.sh
cd ../..

