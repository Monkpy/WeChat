# --*-- coding:utf-8 --*--
import urllib


def StrUrl(put):
    name = put
    url_name = urllib.parse.quote(name)
    print(url_name)
    return url_name


# StrUrl()

