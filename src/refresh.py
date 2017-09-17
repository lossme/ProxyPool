#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-08 23:18:44
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

from proxy_fuzz import fuzz_all, proxy_is_useful
from redis_client import RedisClient
from multiprocessing.dummy import Pool as ThreadPool


class ProxyRefresh():

    def __init__(self, pool_num=10):
        self.https_proxy = RedisClient('https_proxy')
        self.http_proxy = RedisClient('http_proxy')
        self.proxy_list = list(fuzz_all())
        self.pool_num = pool_num

    def refresh_all(self):
        self.refresh_https()
        self.refresh_http()

    def refresh_https(self):
        pool = ThreadPool(self.pool_num)
        pool.map(self.valid_https_task, self.https_proxy.get_all())
        pool.map(self.valid_https_task, self.proxy_list)
        pool.close()
        pool.join()

    def refresh_http(self):
        pool = ThreadPool(self.pool_num)
        pool.map(self.valid_http_task, self.http_proxy.get_all())
        pool.map(self.valid_http_task, self.proxy_list)
        pool.close()
        pool.join()

    def valid_http_task(self, p):
        if proxy_is_useful(p, 'http'):
            self.http_proxy.add(p)
        else:
            self.http_proxy.delete(p)

    def valid_https_task(self, p):
        if proxy_is_useful(p, 'https'):
            self.https_proxy.add(p)
        else:
            self.https_proxy.delete(p)


def main():
    proxy_refresh = ProxyRefresh()
    proxy_refresh.refresh_all()


def run_in_shcedule():
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(main, 'interval', minutes=10)
    sched.start()

if __name__ == '__main__':
    main()
