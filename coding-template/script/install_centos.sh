#!/bin/bash
INSTALL_NAME=coding_template
INSTALL_PATH=/opt/test/${INSTALL_NAME}
if [ "$DB_PORT" = "" ]
then
  DB_PORT=27017
fi

if [ "$LOG_LEVEL" = "" ]
then
  LOG_LEVEL="error"
fi

if [ "$INTERVAL_TIME" = "" ]
then
  INTERVAL_TIME=600
fi


sed -i "s#@DB_HOST@#${DB_HOST}#g" ${INSTALL_PATH}/mongodb.json
sed -i "s#@DB_PORT@#${DB_PORT}#g" ${INSTALL_PATH}/mongodb.json
sed -i "s#@DB_NAME@#${DB_NAME}#g" ${INSTALL_PATH}/mongodb.json
sed -i "s#@USERNAME@#${USERNAME}#g" ${INSTALL_PATH}/mongodb.json
sed -i "s#@PASSWD@#${PASSWD}#g" ${INSTALL_PATH}/mongodb.json
mkdir -p ${INSTALL_PATH}
appc reg -n coding_template -c "${INSTALL_PATH}/coding_template    --${LOG_LEVEL} " -u root -w "${INSTALL_PATH}" -f -t "`date  +\"%Y-%m-%d %H:%M:%S\"`" -i ${INTERVAL_TIME}

