#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-09 00:13:49
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

from flask import Flask
from flask_restful import Resource, Api
from redis_client import RedisClient
from flask_restful import reqparse
app = Flask(__name__)
api = Api(app)

# 状态码
SUCCESS_CODE = 0
PARAM_ERROR = 1


def succ(data=None):
    return {
        "code": SUCCESS_CODE,
        "data": data
    }


def error(error_code, msg=''):
    return {
        "code": error_code,
        "msg": msg
    }


class ProxyManage(Resource):

    def __init__(self):
        self.http_proxy = RedisClient('http_proxy')
        self.https_proxy = RedisClient('https_proxy')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True,
                                 help='required args of proxy type: http/https, like ?type=http')

    def get(self):
        self.parser.add_argument('all', type=str, default='false', required=False, help='')
        get_all = self.parser.parse_args()['all']
        proxy_type = self.parser.parse_args()['type']
        if proxy_type == 'http':
            if get_all == 'true':
                return succ(self.http_proxy.get_all())
            else:
                return succ(self.http_proxy.get_one())
        elif proxy_type == 'https':
            if get_all == 'true':
                return succ(self.https_proxy.get_all())
            else:
                return succ(self.https_proxy.get_one())
        else:
            return error(PARAM_ERROR, 'proxy type param error,must be http/https')

    def delete(self):
        self.parser.add_argument('ip', type=str, required=True,
                                 help='required args of ip: like ?type=http&ip=6.6.6.6:66')

        proxy_type = self.parser.parse_args()['type']
        if proxy_type == 'http':
            return succ(self.http_proxy.delete(ip))
        if proxy_type == 'https':
            return succ(self.https_proxy.delete(ip))
        else:
            self.http_proxy.delete(ip)
            self.https_proxy.delete(ip)
            return succ()


class Welcome(Resource):

    def get(self):
        return succ('ok, now it works!')

api.add_resource(Welcome, '/')
api.add_resource(ProxyManage, '/proxy')

if __name__ == '__main__':
    app.run()
