#!/bin/bash
INSTALL_NAME=appmanager
INSTALL_PATH=/opt/${INSTALL_NAME}

mkdir -p ${INSTALL_PATH}
sh -x ${INSTALL_PATH}/script/watch.sh &

