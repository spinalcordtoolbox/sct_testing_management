#!/bin/bash

#To run this script follow the pattern: ./deploy_dev_version.sh dev_branch backup_file_location backup_filename

# WARNING !!!
# Running the following script will perform a deep Docker prune (delete all containers,images and volumes)
# Any versions of this repository located under ~/devel/ will be removed.

# Get time for performance testing
start=`date +%s`

#Define text formatting
bold=$(tput bold)
green=`tput setaf 2`
normal=$(tput sgr0)

echo "${green}${bold}Purging existing docker images,volumes${normal}"
echo "${green}${bold}-------------------------------------------------------${normal}"

# Delete every Docker containers
# Must be run first because images are attached to containers
docker rm -f $(docker ps -a -q)

# Delete every Docker image
docker rmi -f $(docker images -q)

#Docker system prune
docker system prune -a -f --volumes

#Remove old git repo
rm -rf ~/devel/sct_testing_management

echo "${green}${bold}Setting up git repo to branch $1 ${normal}"
echo "${green}${bold}-------------------------------------------------------${normal}"

#Copy git repo
git clone https://github.com/neuropoly/sct_testing_management.git ~/devel/sct_testing_management

#Change directory to change branch
cd ~/devel/sct_testing_management

#Change branch on git repo
git checkout $1

echo "${green}${bold}Build & start docker containers${normal}"
echo "${green}${bold}-------------------------------------------------------${normal}"

#Build project slack
docker-compose -f ~/devel/sct_testing_management/local.yml build

#Start docker containers
docker-compose -f ~/devel/sct_testing_management/local.yml up -d

#Apply django migrations
docker-compose -f ~/devel/sct_testing_management/local.yml run --rm django python manage.py migrate

#Stop docker containers
docker-compose -f ~/devel/sct_testing_management/local.yml down

#Stop postgres docker container
docker-compose -f ~/devel/sct_testing_management/local.yml up -d postgres

#Get postgres docker container ID
export DOCKERID_POST="$(docker ps --format "{{.ID}}" --filter "name=sct_testing_management_postgres")"

#Copy postgres backup to postgres docker container
docker cp $2 "${DOCKERID_POST}":/backups

#Restore postgres DB from backup
docker-compose -f ~/devel/sct_testing_management/local.yml exec postgres restore $3

#Start docker containers
docker-compose -f ~/devel/sct_testing_management/local.yml up -d

#Create django superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | docker-compose -f ~/devel/sct_testing_management/local.yml run --rm django python manage.py shell

#Get time for performance testing
end=`date +%s`
runtime=$((end-start))

echo "${green}${bold}Deployment executed in ${runtime} seconds ${normal}"
echo "${green}${bold}-------------------------------------------------------${normal}"


echo "${green}${bold}System ready to use${normal}"
echo "${green}${bold}-------------------------------------------------------${normal}"




