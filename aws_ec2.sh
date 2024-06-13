#!/bin/bash

set -x

sudo apt update

sudo apt upgrade

sudo apt install python3-pip

sudo apt install python3-virtualenv

mkdir app

cd app

virtualenv venv

source venv/bin/activate

git clone https://github.com/adventuresoul/campus_connect.git

cd campus_connect

sudo apt install libpq-dev

pip3 install -r requirements.txt

sudo ufw enable

sudo ufw allow 8000

