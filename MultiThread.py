# --*-- coding:utf-8 --*--
import json
import random
import time

import requests
from lxml import etree

from Thread.ParaMeter import paraMeter
from Thread.Str_to_Url import StrUrl


class weChat(object):

    def __init__(self, name):
        self.url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(name)
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "weixin.sogou.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }
        self.GetContentHeaders = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            'Host': 'mp.weixin.qq.com',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }

    def getLinks(self, url):
        """
        :param url: 每一页请求的URL
        :param Next_Page:  翻页链接  目前10页
        :return: 返回详情页的URL
        """
        response = requests.get(url, headers=self.headers)
        cookie = response.cookies.get_dict()
        # print(cookie)
        if response.status_code == 200:
            print(response.text)
            tree = etree.HTML(response.text)
            # Next_Page = tree.xpath('//*[@id="sogou_next"]/@href')
            # if Next_Page:
            #     page_link = 'https://weixin.sogou.com/weixin' + Next_Page[0]
            #     tt = random.randint(1, 2)
            #     time.sleep(tt)
            #     self.getLinks(page_link)
            url_links = tree.xpath('//ul[@class="news-list"]/li/div[2]/h3/a/@href')
            for link in url_links:
                url_link = paraMeter(link)
                return url_link  # 使用yield循环
        else:
            print(response.status_code)

    def getContent(self, href):
        response = requests.get(href)
        print(response.text)
        tree = etree.HTML(response.text)
        Title = tree.xpath('//h2[@id="activity-name"]/text()')
        print(Title)

    def main(self):
        href = self.getLinks(self.url)
        self.getContent(href)


if __name__ == '__main__':
    name = StrUrl('旅游文章')
    wechat = weChat(name)
    wechat.main()


