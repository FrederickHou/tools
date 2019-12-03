#!/usr/bin/ python
# coding=utf-8


import os
import time
import stomp
import json
import logging


WORK_HOME = "/opt/SSO_TO_LDAP_SYNC"
cfg_file = os.path.join(os.getcwd(), "activemq_wrapper.json")
# cfg_file = os.path.join(WORK_HOME, "activemq_wrapper.json")
with open(cfg_file, mode='r') as f:
    config_json = json.loads(f.read())


class Activemq(object):

    TAG = "ACTIVEMQ"
    def __init__(self,lister_name,lister_obj,LOG_TAG):
        self.conn = None
        self.host = config_json.get("host")
        self.port = config_json.get("port")
        self.username = config_json.get("username")
        self.passwd = config_json.get("passwd")
        self.lister_name = lister_name
        self.lister_obj = lister_obj
        self.log = logging.getLogger(LOG_TAG + "." + self.TAG)
        self.__connect()

    def __connect(self):
        self.conn = stomp.Connection([(self.host,self.port)])
        if self.conn:
            self.conn.set_listener(self.lister_name,self.lister_obj)
            self.conn.start()
            self.conn.connect(self.username, self.passwd, wait=True)
        else:
            self.log.error("connect avtiveMQ error")
            raise Exception("connect avtiveMQ error")

    def close(self):
        if self.conn:
            self.conn.disconnect()
            self.conn = None

    def get_message(self,queue_name_or_topic_name,client_id="",headers=None):
        try:
            self.conn.subscribe(destination=queue_name_or_topic_name, id = client_id, ack = 'auto',headers = headers)
        except Exception as e:
            print e

    def send_message(self,queue_name_or_topic_name,body):
        try:
            self.conn.send(queue_name_or_topic_name, body)
        except Exception as e:
            print e


