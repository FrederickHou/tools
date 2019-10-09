#!/bin/bash
check_failed=0
if [ "$DB_HOST" = "" ]
then
  echo "error: Mongodb host ip needed. Please export DB_HOST before install."
  check_failed=1
fi

if [ "$DB_NAME" = "" ]
then
  echo "error: Mongodb database name needed. Please export DB_NAME before install."
  check_failed=1
fi

if [ "$USERNAME" = "" ]
then
  echo "error: Mongodb user name needed. Please export USERNAME before install."
  check_failed=1
fi

if [ "$PASSWD" = "" ]
then
  echo "error: Mongodb password needed. Please export PASSWD before install."
  check_failed=1
fi

if [ $check_failed = 1 ]
then
    exit 1
fi


if [ "$DB_PORT" = "" ]
then
  echo "warnning: Use default DB_PORT '27017'. Please export DB_PORT before install if you want to configure it."
fi

if [ "$INTERVAL_TIME" = "" ]
then
  echo "warnning: Use default INTERVAL_TIME '600'. Please export INTERVAL_TIME before install if you want to configure it."
fi

if [ "$LOG_LEVEL" = "" ]
then
  echo "warnning: Use default LOG_LEVEL 'error'. Please export LOG_LEVEL before install if you want to configure it."
fi

exit 0

