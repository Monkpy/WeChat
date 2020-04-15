# --*-- coding:utf-8 --*--

"""
k/h: 触发事件

(function(){
$("a").on("mousedown click contextmenu",
function(){
var b=Math.floor(100*Math.random())+1,
a=this.href.indexOf("url="),
c=this.href.indexOf("&k=");
-1!==a&&-1===c&&(a=this.href.substr(a+4+parseInt("21")+b,1),
this.href+="&k="+b+"&h="+a)})})();

"""
import random

import requests


def paraMeter(url_str):

	b = int(random.random()*100) + 1

	url = url_str

	a = url.find('url=')
	url_old = url + '&k=' + str(b) + '&h=' + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
	url_new = 'https://weixin.sogou.com' + url_old
	# print(url_new)
	return url_new





