# --*-- coding:utf-8 --*--
import random
import re
import time
from urllib.parse import urlencode

import pymongo
import requests
import uuid as uuid
from lxml import etree

from WeChat import ParaMeter
from WeChat.AbyProxy import Proxy
from WeChat.ParaMeter import paraMeter
from WeChat.Str_to_Url import StrUrl
from WeChat.Str_to_cookie import str_url_dict


class weChat(object):

	def __init__(self, name):
		self.url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(name)
		self.GetLinksHeaders = {
			"Host": "weixin.sogou.com",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "zh-CN,zh;q=0.9",

		}
		self.GetTrueHeaders = {
			"Host": "weixin.sogou.com",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "zh-CN,zh;q=0.9",

		}

	# 获取cookie所需参数，拼接cookie
	def getCookie(self, proxy=None):
		"""
		:param proxy: IP代理，初始使用本机IP
		:param SNUID: cookie标识，记录抓取次数，每个SNUID只能抓取两条，需要建立IP代理池
		:param SUV: 可能是标记翻页，暂时不记
		:param str_url_dict: 请求连接所有的参数
		:return:
		"""
		self.GetLinksHeaders['Referer'] = self.url
		response = requests.get(self.url, headers=self.GetLinksHeaders, proxies=proxy)
		cookie = response.cookies.get_dict()
		iploc = cookie['IPLOC']
		abtest = cookie['ABTEST']
		snuid = cookie['SNUID']
		suid = cookie['SUID']
		ud = uuid.uuid1()
		uigs_t = str(int(round(time.time() * 1000)))
		str_url_dict['uigs_t'] = uigs_t
		str_url_dict['uuid'] = ud
		str_url_dict['snuid'] = snuid
		url = 'https://pb.sogou.com/pv.gif?' + urlencode(str_url_dict)
		resp = requests.get(url)
		ck = resp.cookies.get_dict()
		suv = ck['SUV']
		ck_str = 'SUV=%s; SNUID=%s; SUID=%s; IPLOC=%s; ABTEST=%s' % (suv, snuid, suid, iploc, abtest)  # cookie字符串
		self.GetTrueHeaders['Cookie'] = ck_str
		# print(self.GetLinksHeaders)

	# 获取单页列表数据连接
	def getLinks(self):
		response = requests.get(self.url, headers=self.GetLinksHeaders)
		tree = etree.HTML(response.text)
		url_links = tree.xpath('//ul[@class="news-list"]/li/div[2]/h3/a/@href')
		for link in url_links:
			url = paraMeter(link)  # 构造'真'URL
			yield url

	# 获取真正的连接
	def getTrueLinks(self, href):
		# print(href)
		# print(self.GetLinksHeaders)
		response = requests.get(href, headers=self.GetTrueHeaders)
		tree = etree.HTML(response.text)
		sign = ''.join(tree.xpath('//title/text()'))
		if '¢' in sign:
			try:
				proxy = Proxy()
				print('调用代理获取新的cookie--SNUID')
				self.getCookie(proxy)
				self.getTrueLinks(href)
			except Exception as e:
				if '407 Proxy Authentication Required' in str(e):
					print('Error:获取IP代理失败，重新获取')
					proxy = Proxy()
					print('Error:407,重新请求新的IP代理')
					self.getCookie(proxy)
					self.getTrueLinks(href)
		else:
			url_true = re.findall('url \+= \'(.*?)\'', ''.join(response.text), re.S)
			if url_true:
				url = ''.join(url_true)
				resp = requests.get(url)
				tree = etree.HTML(resp.text)
				content = tree.xpath('//div[@id="js_content"]//text()')
				with open('./html.txt', 'a', encoding='utf-8') as f:
					f.write(str(content) + '\r\n')
					print('======================')

	def main(self):
			self.getCookie()
			for href in self.getLinks():
				self.getTrueLinks(href)


if __name__ == '__main__':
	name = StrUrl('旅游')
	wechat = weChat(name)
	wechat.main()




