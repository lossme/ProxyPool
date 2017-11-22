# -*- coding: utf-8 -*-
# @Date    : 2017-11-21 16:59:43
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme


class APIBaseException(Exception):
    msg = 'server error'
    request = ''
    error_code = 1000

    def __init__(self, msg=None, request=None):
        if msg is not None:
            self.msg = msg
        if request is not None:
            self.request = request

    def __repr__(self):
        return 'msg=%s request=%s' % (self.msg, self.request)

    def __str__(self):
        return 'msg=%s request=%s' % (self.msg, self.request)


class ParamError(APIBaseException):
    msg = 'param error'
    error_code = 1001
