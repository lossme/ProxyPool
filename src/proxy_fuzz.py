# -*- coding: utf-8 -*-
# @Date    : 2017-09-06 10:33:46
# @Author  : Key
# @Email   : 1612730560@qq.com
# @Link    : https://github.com/lossme

import requests
import requests.exceptions
import execjs
import re
from lxml import etree
import socket
try:
    import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

TIMEOUT = 15
HEADERS = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }
socket.setdefaulttimeout(TIMEOUT)

# 验证ip合法性(6.6.6.6 / 6.6.6.6:666)
verify_ip_re = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)(:(\d{1,5}))?$')


def xici(page=5):
    """
    抓取西刺代理 http://www.xicidaili.com/
    @param: 翻页数
    @return:
    """
    url_list = ('http://www.xicidaili.com/nn/{0}'.format(i) for i in range(1, page + 1))
    for url in url_list:
        html = requests.get(url=url, headers=HEADERS).content.decode('utf-8')
        html_tree = etree.HTML(html)
        proxy_list = html_tree.xpath('.//table[@id="ip_list"]//tr')
        for proxy in proxy_list[1:]:
            yield ':'.join(proxy.xpath('./td/text()')[0:2])


def kuaidaili(page=5):
    """
    抓取快代理IP http://www.kuaidaili.com/
    @param page: 翻页数
    @return:
    参考博文https://my.oschina.net/jhao104/blog/865966
    """
    def executejs(html):
        # 提取其中执行JS函数的参数
        js_string = ''.join(re.findall(r'(function .*?)</script>', html))
        js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', html))

        js_name = re.findall(r'function (\w+)', js_string)[0]
        # 修改JS函数，使其返回Cookie内容
        js_string = js_string.replace('eval("qo=eval;qo(po);")', 'return po')
        func = execjs.compile(js_string)
        return parse_cookie(func.call(js_name, js_arg))

    def parse_cookie(string):
        string = string.replace("document.cookie='", "")
        clearance = string.split(';')[0]
        return {clearance.split('=')[0]: clearance.split('=')[1]}

    base_url = 'http://www.kuaidaili.com/proxylist/{0}/'
    html = requests.get(url=base_url.format(1), headers=HEADERS).content.decode('utf-8')
    try:
        cookie = executejs(html)
    except Exception:
        cookie = None
    url_list = (base_url.format(i) for i in range(1, page + 1))
    for url in url_list:
        html = requests.get(url=url, headers=HEADERS, cookies=cookie).content.decode('utf-8')
        html_tree = etree.HTML(html)
        proxy_list = html_tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
        for proxy in proxy_list:
            yield ':'.join(proxy.xpath('./td/text()')[0:2])


def liuliuip(proxy_number=100):
    """
    抓取代理66 http://www.66ip.cn/
    @param proxy_number: 代理数量
    @return:
    """
    url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
        proxy_number)
    html = requests.get(url=url, headers=HEADERS).content.decode('gbk')
    for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
        yield proxy


def youdaili(days=1):
    """
    抓取有代理 http://www.youdaili.net/Daili/http/
    @param: days
    @return:
    """
    url = "http://www.youdaili.net/Daili/http/"
    html = requests.get(url=url, headers=HEADERS).content.decode('utf-8')
    html_tree = etree.HTML(html)
    page_url_list = html_tree.xpath('.//div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
    for page_url in page_url_list:
        html = requests.get(page_url, headers=HEADERS).content.decode('utf-8')
        proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
        for proxy in proxy_list:
            yield proxy


def goubanjia():
    """
    抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
    @param:
    @return:
    """
    url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
    for page in range(1, 10):
        page_url = url.format(page=page)
        html = requests.get(url=url, headers=HEADERS).content.decode('utf-8')
        html_tree = etree.HTML(html)
        proxy_list = html_tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                            and not(contains(@style, 'display:none'))
                            and not(contains(@class, 'port'))
                            ]/text()
                    """
        for each_proxy in proxy_list:
            # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
            ip_addr = ''.join(each_proxy.xpath(xpath_str))
            port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
            yield '{}:{}'.format(ip_addr, port)


def xdaili():
    """
    抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
    @return:
    """
    url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
    r = requests.get(url, headers=HEADERS)
    rows = r.json()['RESULT']['rows']
    for row in rows:
        yield '{}:{}'.format(row['ip'], row['port'])


def proxy_is_useful(proxy, proxy_type='https', timeout=10):
    """
    检验代理是否可用
    @proxy: '6.6.6.6:666'
    @timeout: 超时时间
    @return: boolen
    """
    url = 'https://www.baidu.com'
    if proxy_type == 'http':
        url = 'http://www.google.cn/'
        proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    else:
        proxies = {"https": "https://{proxy}".format(proxy=proxy)}
    try:
        if verify_ip_re.match(proxy):
            r = requests.get(url, proxies=proxies, timeout=timeout, verify=False)
            if r.status_code == 200:
                return True
    except Exception:
        pass
    return False


def fuzz_all():
    yield from xici()
    yield from kuaidaili()
    yield from liuliuip()
    yield from youdaili()
    yield from goubanjia()


def fuzz_all_valid(proxy_type='https'):
    for p in fuzz_all():
        if proxy_is_useful(p, proxy_type):
            yield p
