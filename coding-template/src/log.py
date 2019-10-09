#!/usr/bin/ python
#coding:utf-8
'''
@DATE:2019/07/17
@AUTHOR:Frederick hou
@Function: user sync
'''

import logging
import os
from logging.handlers import RotatingFileHandler

class LOG(object):

    def __init__(self,args,log_folder_path,LOG_TAG,max_M = 20,backup_count = 5):

        log_level = logging.ERROR
        if args.debug:
            log_level = logging.DEBUG
        elif args.info:
            log_level = logging.INFO
        elif args.warn:
            log_level = logging.WARNING
        elif args.error:
            log_level = logging.ERROR
        logMaxBytes = max_M * 1024 * 1024
        logBackupCount = backup_count
        if not os.path.exists(log_folder_path) :
            try:
                os.mkdir(log_folder_path,0777)
                os.chmod(log_folder_path,0777)
            except Exception as e:
                return
        self.logger = logging.getLogger(LOG_TAG)
        self.logger.setLevel(log_level)
        rHandler = RotatingFileHandler('%s%s.log' % (log_folder_path, LOG_TAG),
                                    maxBytes=logMaxBytes, backupCount=logBackupCount)
        rHandler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[%(lineno)d] %(message)s')
        rHandler.setFormatter(formatter)
        self.logger.addHandler(rHandler)
