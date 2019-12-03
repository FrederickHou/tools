
FROM centos
MAINTAINER frederick_hou@163.com

ENV WORK_HOME /opt/appmanager

RUN mkdir -p $WORK_HOME;

ADD /src/*.py $WORK_HOME/

RUN 
    yum -y install epel-release;\
    yum -y install python-pip;\
    yum -y install openldap-devel;\
    yum -y install python-devel;\
    yum -y install gcc;\
    pip install flask;  
     
WORkDIR $WORK_HOME/

CMD python $WORK_HOME/main.py
