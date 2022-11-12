#!/bin/bash
sudo apt-get update -y &&
sudo apt-get install -y \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" &&
sudo apt-get update -y &&
sudo sudo apt-get install docker-ce docker-ce-cli containerd.io -y &&
sudo usermod -aG docker ubuntu &&
sudo git clone --single-branch --branch implementation https://github.com/mvww11/data-workflow-01.git /var/tmp/data-workflow-01 &&
sudo docker pull mvww11/daredata:latest &&
sudo docker run -d -p 5000:5000 -v /var/tmp/data-workflow-01:/data-workflow-01 mvww11/daredata:latest