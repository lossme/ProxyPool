# -*- coding: utf-8 -*-
# @Date    : 2017-09-09 00:13:49
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

from flask import Flask
from flask_restful import Resource, Api
from redis_client import RedisClient
from flask_restful import reqparse

from exceptions import APIBaseException, ParamError

app = Flask(__name__)
api = Api(app)


def error_handle(func):
    def wraper(*args, **kwargs):
        try:
            return {'code': 0, 'data': func()}
        except APIBaseException as e:
            return {'code': e.error_code, 'request': e.request, 'msg': e.msg}


class ProxyManage(Resource):

    def __init__(self):
        self.http_proxy = RedisClient('http_proxy')
        self.https_proxy = RedisClient('https_proxy')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True,
                                 help='required args of proxy type: http/https, like ?type=http')

    @error_handle
    def get(self):
        self.parser.add_argument('all', type=str, default='false', required=False, help='')
        get_all = self.parser.parse_args()['all']
        proxy_type = self.parser.parse_args()['type']
        if proxy_type == 'http':
            if get_all == 'true':
                return self.http_proxy.get_all()
            else:
                return self.http_proxy.get_one()
        elif proxy_type == 'https':
            if get_all == 'true':
                return self.https_proxy.get_all()
            else:
                return self.https_proxy.get_one()
        else:
            raise ParamError(msg='proxy type param error,must be http/https')

    @error_handle
    def delete(self):
        self.parser.add_argument('ip', type=str, required=True)

        args = self.parser.parse_args()

        proxy_type = args.get('type')
        ip = args.get('ip')
        if proxy_type == 'http':
            return self.http_proxy.delete(ip)
        if proxy_type == 'https':
            return self.https_proxy.delete(ip)
        else:
            self.http_proxy.delete(ip)
            self.https_proxy.delete(ip)
            return


class Welcome(Resource):

    @error_handle
    def get(self):
        return 'ok, now it works!'

api.add_resource(Welcome, '/')
api.add_resource(ProxyManage, '/proxy')

if __name__ == '__main__':
    app.run()
