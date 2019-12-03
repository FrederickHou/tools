#!/usr/bin/ python
#coding:utf-8

'''
@DATE:2019/09/04
@AUTHOR:Frederick hou
@Function: class MongoDB,provide mongo database operate interface.
'''

import pymongo
import os
import json
from pymongo import MongoClient
import logging

cfg_file = os.path.join(os.getcwd(), "mongodb.json")
with open(cfg_file, mode='r') as f:
    config_json = json.loads(f.read())


class MongoDB(object):
  
    TAG = "MongoDB"

    def __init__(self,LOG_TAG="None"):
        self.client = MongoClient("{}:{}".format(config_json.get("db_host","127.0.0.1"),config_json.get("db_port",27017)))
        db_name = config_json.get("db_name","admin")
        username = config_json.get("username")
        passwd = config_json.get("passwd")
        self.log = logging.getLogger(LOG_TAG + "." + self.TAG)
        if username and passwd:
            if not self.client[db_name].authenticate(username ,passwd,mechanism='SCRAM-SHA-1'):
                raise Exception("authenticate fail  username:<{}> password:<{}>".format(username,passwd))
            self.log.debug("mongodb username:<{}> password:<{}> authenticate success".format(username,passwd))
            db_list = self.client.list_database_names()
            if not db_name in db_list:
                raise Exception("database <{}> don't exists".format(db_name))
        self.db = self.client[db_name]

    def if_table_exists(self,collection):
        table_list = self.db.list_collection_names()
        if not collection in table_list:
            self.log.error("collection:<{}> does not exists.")
            return False
        else:
            self.log.debug("collection:<{}>  exists.")
            return True        

    def insert_one(self,collection, data):
        self.collection = self.db[collection]
        res = BaseHandle.insert_one(self.collection, data)
        return res

    def insert_many(self,collection, data_list):
        self.collection = self.db[collection]
        res = BaseHandle.insert_many(self.collection, data_list)
        return res

    def find_one(self,collection, data, data_field={}):
        self.collection = self.db[collection]
        res = BaseHandle.find_one(self.collection, data, data_field)
        return res

    def find_many(self, collection,data, data_field={}):
        """ 有多个键值的话就是 AND 的关系"""
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_all(self, collection,data={}, data_field={}):
        """select * from collection"""
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_in(self, collection,field, item_list, data_field={}):
        """SELECT * FROM collection WHERE field in ("A", "D")"""
        data = dict()
        data[field] = {"$in": item_list}
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_or(self, collection,data_list, data_field={}):
        """db.inventory.find(
    {"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})

        SELECT * FROM inventory WHERE status = "A" OR qty < 30
        """
        data = dict()
        data["$or"] = data_list
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_between(self,collection, field, value1, value2, data_field={}):
        """获取俩个值中间的数据"""
        '''
        seletc * from collection where field between value1 and value2
        '''

        data = dict()
        data[field] = {"$gt": value1, "$lt": value2}
        self.collection = self.db[collection]
        # data[field] = {"$gte": value1, "$lte": value2} # <>   <= >=
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_more(self, collection,field, value, data_field={}):
        data = dict()
        data[field] = {"$gt": value}
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_less(self,collection, field, value, data_field={}):
        data = dict()
        data[field] = {"$lt": value}
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_like(self, collection,field, value, data_field={}):
        """ where key like "%audio% """
        data = dict()
        data[field] = {'$regex': '.*' + value + '.*'}
        self.collection = self.db[collection]
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def query_limit(self, query, num):
        """db.collection.find(<query>).limit(<number>) 获取指定数据"""
        res = query.limit(num)
        return res

    def query_count(self, query):
        res = query.count()
        return res

    def query_skip(self, query, num):
        res = query.skip(num)
        return res

    def query_sort(self, query, data):
        """db.orders.find().sort( { amount: -1 } ) 根据amount 降序排列"""
        res = query.sort(data)
        return res

    def delete_one(self, collection,data):
        """ 删除单行数据 如果有多个 则删除第一个"""
        self.collection = self.db[collection]
        res = BaseHandle.delete_one(self.collection, data)
        return res

    def delete_many(self,collection, data):
        """ 删除查到的多个数据 data 是一个字典 """
        self.collection = self.db[collection]
        res = BaseHandle.delete_many(self.collection, data)
        return res

    def close(self):
        self.client.close()



class BaseHandle(object):
    @staticmethod
    def insert_one(collection, data):
        """直接使用insert() 可以插入一条和插入多条 不推荐 明确区分比较好"""
        res = collection.insert_one(data)
        return res.inserted_id

    @staticmethod
    def insert_many(collection, data_list):
        res = collection.insert_many(data_list)
        return res.inserted_ids

    @staticmethod
    def find_one(collection, data, data_field={}):
        if len(data_field):
            res = collection.find_one(data, data_field)
        else:
            res = collection.find_one(data)
        return res

    @staticmethod
    def find_many(collection, data, data_field={}):
        """ data_field 是指输出 操作者需要的字段"""
        if len(data_field):
            res = collection.find(data, data_field)
        else:
            res = collection.find(data)
        return res

    @staticmethod
    def update_one(collection, data_condition, data_set):
        """修改一条数据"""
        res = collection.update_one(data_condition, data_set)
        return res

    @staticmethod
    def update_many(collection, data_condition, data_set):
        """ 修改多条数据 """
        res = collection.update_many(data_condition, data_set)
        return res

    @staticmethod
    def replace_one(collection, data_condition, data_set):
        """ 完全替换掉 这一条数据， 只是 _id 不变"""
        res = collection.replace_one(data_condition, data_set)
        return res

    @staticmethod
    def delete_many(collection, data):
        res = collection.delete_many(data)
        return res

    @staticmethod
    def delete_one(collection, data):
        res = collection.delete_one(data)
        return res


if __name__ == "__main__":
    mongdb_obj = MongoDB()
    # results = mongdb_obj.find_many("host_resource_collection",{"fs.usage": {"$gt":0.9}},{"_id":0,"host_name":1,"create_time":1,"fs.$":1}).pretty() 
    # mongdb_obj.query_sort(results,[('create_time',-1)])
    # for x in results:
    #     print x
    collection = mongdb_obj.db["host_resource_collection"]
    results = collection.aggregate(
        [
        {"$unwind":"$fs"},
        {"$match":{"fs.usage": {"$gt":0.9},"create_time":{"$gt": "2019-09-11 00:00:00", "$lt": "2019-09-12 00:00:00"}}},      
        {"$project":{"_id":0,"host_name":1,"create_time":1,"fs":1}},
        {"$sort":{"create_time":-1}}])
    for x in results:
        print x    