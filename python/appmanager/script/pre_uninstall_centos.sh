#!/bin/bash

for i in $(ps aux | grep -w /opt/appmanager | grep -v grep  | awk '{print $2}')
	do
		kill -9 $i
done