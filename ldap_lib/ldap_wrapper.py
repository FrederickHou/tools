#!/usr/bin/ python
#coding:utf-8

'''
@DATE:2019/07/17
@AUTHOR:Frederick hou
@Function: ldap database interface:
    1.ldap_search()
    2.add_user()
    3.modify_user()
    4.delete_user()
'''

import time
import ldap
import os
import json
import logging
WORK_HOME = "/opt/SSO_TO_LDAP_SYNC"
cfg_file = os.path.join(os.getcwd(), "ldap_wrapper.json")
# cfg_file = os.path.join(WORK_HOME, "ldap_wrapper.json")
with open(cfg_file, mode='r') as f:
    config_json = json.loads(f.read())

class Ldap(object):

    TAG = "LDAP"

    def __init__(self, LOG_TAG=None):
        self.server_uri = config_json.get("ldap_host","127.0.0.1") 
        self.server_port = config_json.get("ldap_port","389")
        self.username = config_json.get("username","admin")
        self.passwd = config_json.get("passwd","admin")
        self.org = config_json.get("org","example.com") 
        self.ldap_obj = None
        self.dn = "cn={0},dc={1},dc={2}".format(self.username,self.org.split(".")[-2],self.org.split(".")[-1])
        self.log = logging.getLogger(LOG_TAG + "." + self.TAG)
        self.ldap_connect(self.dn, self.passwd)
        

    def ldap_connect(self, bind_name='', bind_passwd=''):
        """
        :param bind_name: "cn=admin,dc=example,dc=org"
        :param bind_passwd:
        :return:
        """
        url = "ldap://" + self.server_uri + ":" + str(self.server_port)
        try:
            conn = ldap.initialize(url)
        except Exception as e:
            self.log.error("ldap init error :{}".format(e))
            print "ldap init error :{}".format(e)
            raise Exception("init LDAP error,please check url")
        if not bind_name or not bind_passwd:
            self.log.error("bind_name or bind_passwd is None")
            print "bind_name or bind_passwd is None"
            raise Exception("bind_name or bind_passwd is None")
        try:
            rest = conn.simple_bind_s(bind_name, bind_passwd)
        except ldap.SERVER_DOWN:
            self.log.error("Can't connect to LDAP, bind fail")
            print "Can't connect to LDAP, bind fail"
            raise Exception("Can't connect to LDAP, bind fail")
        except ldap.INVALID_CREDENTIALS:
            self.log.error("LDAP account error")
            print "LDAP account error"
            raise Exception("LDAP account error")
        except Exception as e:
            self.log.error("LDAP account error {}".format(e))
            print "LDAP account error {}".format(e)
            raise Exception(type(e))
        if rest[0] != 97:  # 97 it's mean success
            self.log.error("LDAP connect fail")
            print "LDAP connect fail"
            raise Exception(rest[1])
        self.ldap_obj = conn

    def ldap_search(self,username, base='', rdn='cn'):
        """
        base:  ou=test, dc=test, dc=com or dc=test, dc=com
        username: search dest user
        rdn: cn/ou
        return: bool,list
        """
        scope = ldap.SCOPE_SUBTREE
        filter = "%s=%s" % (rdn, username)
        retrieve_attributes = None
        try:
            result_id = self.ldap_obj.search(base, scope, filter, retrieve_attributes)
            result_type, result_data = self.ldap_obj.result(result_id)
            if not result_data:
                self.log.debug("LDAP search result_data: {}".format(result_data))
                print "LDAP search result_data: {}".format(result_data)
                return False, []
        except ldap.LDAPError, error_message:
            self.log.error("LDAP search error {}".format(error_message))
            print "LDAP search error {}".format(error_message)
            raise Exception(error_message)
        self.log.debug("LDAP search result_data: {}".format(result_data))
        print "LDAP search result_data: {}".format(result_data)
        return True, result_data      

    def add_user(self, base_dn, password,**kwargs):
        """
        base_dn: cn=test, ou=people,dc=test,dc=com  （NOT NONE）
        password: username password   
        return: bool,int    
        """
        if not base_dn or not password:
            self.log.error("base_dn or password can't empty")
            print "base_dn or password can't empty"
            raise ValueError(u"base_dn or password can't empty")
        dn_list = base_dn.split(',')
        user_info = dict()
        for item in dn_list:
            attr, value = item.split('=')
            if not value:
                self.log.error("DN input error:attribute is empty")
                print "DN input error:attribute is empty"
                raise ValueError(u"DN input error:attribute is empty")
            user_info[attr] = value
        add_record = [('objectclass', ['person', 'inetOrgPerson','organizationalPerson']),
                      ('cn', ['%s' % user_info.get("cn")]),
                      ('sn', ['%s' % user_info.get("cn")]),
                      ("ou",['%s' % user_info.get("ou",None)]),
                      ("uid",['%s' % kwargs.get("uid",None)]),
                      ("mobile",['%s' % kwargs.get("mobile",None)]),
                      ("mail",['%s' % kwargs.get("mail",None)]),
                      ('userpassword', ['%s' % password])]
        try:
            result = self.ldap_obj.add_s(base_dn, add_record)
        except ldap.ALREADY_EXISTS:
            self.log.error("LDAP add user already exists DN:<{}>".format(base_dn))
            print "LDAP add user already exists DN:<{}>".format(base_dn)
            return False, 0
        except ldap.LDAPError, error_message:
            self.log.error("LDAP add user error {}".format(error_message))
            print "LDAP add user error {}".format(error_message)
            raise (error_message)
        else:
            if result[0] == 105:
                self.log.debug("LDAP add user success: DN:<{}> PW:<{}>".format(base_dn,password))
                print "LDAP add user success: DN:<{}> PW:<{}>".format(base_dn,password)
                return True, 1
            else:
                self.log.debug("LDAP add user fail: DN:<{}> PW:<{}>".format(base_dn,password))
                print "LDAP add user fail: DN:<{}> PW:<{}>".format(base_dn,password)
                return False, -1

    def modify_user(self, dn, attr_list):
        """
        MOD_ADD: if this attribute exists,then this attribute will have multi value ,the old value still exists
        MOD_DELETE ：if this attribute exists then delete it 
        MOD_REPLACE ：all of this attribute value will be deleted and the new value will be added
        dn: cn=test, ou=test,dc=test, dc=com
        attr_list: [( ldap.MOD_REPLACE, 'givenName', 'Francis' ),
                    ( ldap.MOD_ADD, 'cn', 'Frank Bacon' )
                   ]
        return:bool,int
        """
        try:
            result = self.ldap_obj.modify_s(dn, attr_list)
        except ldap.LDAPError, error_message:
            self.log.error("LDAP modify user error {}".format(error_message))
            print "LDAP modify user error {}".format(error_message)
            raise (error_message)
        else:
            if result[0] == 103:
                self.log.debug("LDAP modify user success DN:<{}>".format(dn))
                print "LDAP modify user success DN:<{}>".format(dn)
                return True, 1
            else:
                self.log.debug("LDAP modify user fail DN:<{}>".format(dn))
                print "LDAP modify user fail DN:<{}>".format(dn)
                return False, -1

    def delete_user(self, dn):
        """
        dn: cn=test, ou=magicstack,dc=test, dc=com
        return: bool,int
        """
        try:
            result = self.ldap_obj.delete_s(dn)
        except ldap.NO_SUCH_OBJECT:
            self.log.error("LDAP no such user info: <{}>".format(dn))
            print "LDAP no such user info: <{}>".format(dn)
            return False, -2
        except ldap.LDAPError, error_message:
            self.log.error("LDAP delete error {}",format(error_message))
            print "LDAP delete error {}",format(error_message)
            raise (error_message)
        else:
            if result[0] == 107:
                self.log.debug("LDAP delete success DN:<{}>".format(dn))
                print "LDAP delete success DN:<{}>".format(dn)
                return True, 1
            else:
                self.log.error("LDAP delete fail DN:<{}>".format(dn))
                print "LDAP delete fail DN:<{}>".format(dn)
                return False, -1

    def add_group(self,base_dn):
        group_info = dict()
        dn_list = base_dn.split(',')    
        for item in dn_list:
            attr, value = item.split('=')
            if not value:
                self.log.error("DN input error:attribute is empty")
                print "DN input error:attribute is empty"
                raise ValueError(u"DN input error:attribute is empty")
            group_info[attr] = value 
        add_record = [('objectclass', ['organizationalUnit', 'top']),
                        ('ou', ['%s' % group_info.get("ou")])]
        try:
            result = self.ldap_obj.add_s(base_dn, add_record)
        except ldap.ALREADY_EXISTS:
            self.log.error("LDAP add organizationalUnit already exists DN:<{}>".format(base_dn))
            print "LDAP add organizationalUnit already exists DN:<{}>".format(base_dn)
            return False, 0
        except ldap.LDAPError, error_message:
            self.log.error("LDAP add organizationalUnit error {}".format(error_message))
            print "LDAP add organizationalUnit error {}".format(error_message)
            raise (error_message)
        else:
            if result[0] == 105:
                self.log.debug("LDAP add organizationalUnit success: DN:<{}>".format(base_dn))
                print "LDAP add organizationalUnit success: DN:<{}>".format(base_dn)
                return True, 1
            else:
                self.log.debug("LDAP add organizationalUnit fail: DN:<{}> ".format(base_dn))
                print "LDAP add organizationalUnit fail: DN:<{}>".format(base_dn)
                return False, -1                