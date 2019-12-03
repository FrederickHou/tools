# coding-template
---

## INTRODUCE:

**Based on the open source module appmanager as a daemon process python background development template to improve module development efficiency and standardization.**


## BASIC INSTALL:


   CENTOS: yum -y install https://github.com/laoshanxi/app-manager/releases/download/v1.4/appmanager-1.4.4-1.x86_64.rpm

   UBUNTU: apt -f install https://github.com/laoshanxi/app-manager/releases/download/v1.4/appmanager_1.4.4_amd64.deb

## PACKAGE:

    >>  git clone https://github.com/FrederickHou/tools.git
    >>  cd coding-template
    >>  make


## PACKAGE INSTALL:

export DB_HOST="127.0.0.1"
export DB_PORT=27017
export DB_NAME="host_resource"
export USERNAME="host_resource"
export PASSWD="host_resource"
export INTERVAL_TIME=300
export LOG_LEVEL="debug"
    
    CENTOS:  yum -y install ./coding-template-1.0-1.x86_64.rpm            
	UBUNTU:  apt -f install ./coding-template-1.0-1.x86_64.deb

## PACKAGE UNINSTALL: 

    CENTOS:  yum -y remove coding-template
	UBUNTU:  apt -f remove coding-template
