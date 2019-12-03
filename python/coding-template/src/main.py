#!/usr/bin/ python
#coding:utf-8

'''
@DATE:2019/10/09
@AUTHOR:Frederick hou
@Function: coding template
'''

import time
import datetime
import argparse
import os
import sys
import json
from log import LOG


BUILD_DATE = '__BUILD_DATE__'
BUILD_VERSION = '__BUILD_VERSION__'
LOG_TAG = "coding-template"
LOG_FOLDER_PATH = "{}/log/".format(os.getcwd())

def args_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help ="soft version",action = "store_true")
    parser.add_argument("--debug", help = "print message with level DEBUG",action = 'store_true')
    parser.add_argument('--info', help='print message with level INFO',action = 'store_true')
    parser.add_argument('--warn', action='store_true', help='print message with level WARNING')
    parser.add_argument('--error', action='store_true', help='print message with level ERROR')
    args = parser.parse_args()
    return args

# cxfreeze打包时要去掉此判断
# if __name__ == "__main__":

args = args_init()
if args.version:
    print "{}: {},{}".format(LOG_TAG,BUILD_VERSION,BUILD_DATE)
    sys.exit(0)
log_obj = LOG(args,LOG_FOLDER_PATH,LOG_TAG)
try:
   '''
    coding
   '''
   pass
except Exception as e:
    print e
    log_obj.logger.error("exception error:<{}>".format(e))



