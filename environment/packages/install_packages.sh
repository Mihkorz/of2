#!/bin/bash

if (( $EUID != 0 )); then
    echo "This script must be run as root"
    exit 1
fi

if [ ! -f /etc/apt/sources.list.d/R.list ]; then
    echo "Adding R PPA..."

    OS_CODENAME=$(lsb_release --codename | cut -f2)

    # Add R repository
    echo "deb http://cran.r-project.org/bin/linux/ubuntu $OS_CODENAME/" > /etc/apt/sources.list.d/R.list

    # Add secure key
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

    apt-get update
fi

echo "Installing required packages..."
apt-get install -y $(cat packages.list | grep -v "^#")
