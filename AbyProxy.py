# -*- coding:utf-8 -*-


def Proxy():
	# 阿布云代理服务器
	proxyHost = "http-dyn.abuyun.com"
	proxyPort = "9020"

	# 代理隧道验证信息
	proxyUser = "账号"
	proxyPass = "密钥"

	proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
	  "host" : proxyHost,
	  "port" : proxyPort,
	  "user" : proxyUser,
	  "pass" : proxyPass,
	}

	proxies = {
		"http": proxyMeta,
		"https": proxyMeta,
	}
	return proxies






