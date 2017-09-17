#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-07 15:38:43
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

import redis


class RedisClient():

    def __init__(self, key, host='localhost', port=6379, passwd=None, db=0):
        self.__conn = redis.Redis(host=host, port=port, db=db)
        self.key = key

    def add(self, value):
        return self.__conn.sadd(self.key, value)

    def get(self, num=1):
        return list(map(lambda x: x.decode('utf8'), self.__conn.srandmember(self.key, num)))

    def get_one(self):
        res = self.get(num=1)
        if len(res) > 0:
            return res[0]

    def get_all(self):
        return list(map(lambda x: x.decode('utf8'), self.__conn.smembers(self.key)))

    def pop(self):
        return self.__conn.spop(self.key).decode('utf8')

    def delete(self, value):
        return self.__conn.srem(self.key, value)

    def change_key(self, key):
        self.key = key
