#!/bin/bash

if (( $EUID != 0 )); then
   echo "This script must be run as root"
   exit 1
fi

# Add R repository
echo "deb http://cran.r-project.org/bin/linux/ubuntu trusty/" > /etc/apt/sources.list.d/R.list
# Add secure key
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

apt-get update

apt-get install -y $(cat pkg.list | grep -v "^#")
