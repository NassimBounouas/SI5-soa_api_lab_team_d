#!/bin/bash

##########################################
#      ORDERING DATABASE AND SERVICE     #
##########################################

echo "### Building Ordering database image ###"

cd Ordering_Service/Database/
docker build -t uberoolab/team-d-ordering-database .

echo "### Pushing Ordering database image to docker hub ###"
docker push uberoolab/team-d-ordering-database

echo "### Building Ordering service image ###"
cd ../Service
docker build -t uberoolab/team-d-ordering-service .

echo "### Pushing Ordering service image to docker hub ###"
docker push uberoolab/team-d-ordering-service
cd ../../


##########################################
#      MENU DATABASE AND SERVICE         #
##########################################
echo "### Building Menu database image ###"

cd Menu_Service/Database/
docker build -t uberoolab/team-d-menu-database .

echo "### Pushing Menu database image to docker hub ###"
docker push uberoolab/team-d-menu-database

echo "### Building Menu service image ###"
cd ../Service
docker build -t uberoolab/team-d-menu-service .

echo "### Pushing Ordering service image to docker hub ###"
docker push uberoolab/team-d-menu-service
cd ../../

##########################################
#              ETA SERVICE               #
##########################################
echo "### Building ETA service image ###"
cd ETA_Computer_Service/Service
docker build -t uberoolab/team-d-eta-computer-service .

echo "### Pushing ETA service image to docker hub ###"
docker push uberoolab/team-d-eta-computer-service
cd ../../

##########################################
#    DELIVERY DATABASE AND SERVICE       #
##########################################
echo "### Building Delivery database image ###"

cd Delivery_Service/Database/
docker build -t uberoolab/team-d-delivery-database .

echo "### Pushing Delivery database image to docker hub ###"
docker push uberoolab/team-d-delivery-database

echo "### Building Delivery service image ###"
cd ../Service
docker build -t uberoolab/team-d-delivery-service .

echo "### Pushing Delivery  service image to docker hub ###"
docker push uberoolab/team-d-delivery-service
cd ../../

##########################################
#    RESTAURANT DATABASE AND SERVICE     #
##########################################
echo "### Building Restaurant database image ###"

cd Restaurant_Service/Database/
docker build -t uberoolab/team-d-restaurant-database .

echo "### Pushing Restaurant database image to docker hub ###"
docker push uberoolab/team-d-restaurant-database

echo "### Building Restaurant service image ###"
cd ../Service
docker build -t uberoolab/team-d-restaurant-service .

echo "### Pushing Restaurant service image to docker hub ###"
docker push uberoolab/team-d-restaurant-service
cd ../../

##########################################
#              PAYWALL SERVICE           #
##########################################
echo "### Building Payment service image ###"
cd Payment_Service/Service
docker build -t uberoolab/team-d-payment-service .

echo "### Pushing Payment service image to docker hub ###"
docker push uberoolab/team-d-payment-service
cd ../../

##########################################
#          API GATEWAY  SERVICE          #
##########################################
echo "### Building API Gateway service image ###"
cd UberooApiGateway/Service
docker build -t uberoolab/team-d-apigateway .

echo "### Pushing API Gateway service image to docker hub ###"
docker push uberoolab/team-d-apigateway
cd ../../
