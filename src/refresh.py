#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-08 23:18:44
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

from proxy_fuzz import fuzz_all, proxy_is_useful
from redis_client import RedisClient
from multiprocessing.dummy import Pool as ThreadPool
import asyncio


class ProxyRefresh():

    def __init__(self, proxy_type='https'):
        if proxy_type == 'https':
            self.redis_handler = RedisClient('https_proxy')
        elif proxy_type == 'http':
            self.redis_handler = RedisClient('http_proxy')
        else:
            raise Exception('type must be https or http')
        self.proxy_type = proxy_type
        self.proxy_pool = set([*fuzz_all(), *self.redis_handler.get_all()])

    def refresh(self, pool_num=10):
        pool = ThreadPool(pool_num)
        pool.map(self.valid_ip, self.proxy_pool)
        pool.close()
        pool.join()

    def refresh_in_async(self):
        asynctask = AsyncTask()
        for ip in self.proxy_pool:
            asynctask.add_task(self.valid_ip, ip)
        asynctask.run()

    def valid_ip(self, ip):
        if proxy_is_useful(ip, self.proxy_type):
            self.redis_handler.add(ip)
        else:
            self.redis_handler.delete(ip)


class AsyncTask():

    def __init__(self):
        self.__tasks = []
        self.__loop = asyncio.get_event_loop()

    def add_task(self, func, *args, **kwargs):
        task = asyncio.ensure_future(self.run_async(func, *args, **kwargs))
        self.__tasks.append(task)

    async def run_async(self, func, *args, **kwargs):
        future1 = self.__loop.run_in_executor(None, func, *args, **kwargs)
        return await future1

    def run(self):
        res = self.__loop.run_until_complete(asyncio.wait(self.__tasks))
        self.__tasks = []
        return res

    def __del__(self):
        self.__loop.close()


def main():
    proxy_refresh = ProxyRefresh()
    proxy_refresh.refresh_in_async()


def run_in_shcedule():
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(main, 'interval', minutes=10)
    sched.start()


if __name__ == '__main__':
    main()
