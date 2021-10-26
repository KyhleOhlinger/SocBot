#!/bin/bash

# PGP key installation
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key D88E42B4
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 3D99BB18562CBC1C
# Alternative PGP key installation
# wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Debian repository configuration
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list

# Install https support for apt
sudo apt install apt-transport-https

# Elasticsearch installation
sudo apt update && sudo apt install elasticsearch


# Create and start the ES service
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl status elasticsearch.service