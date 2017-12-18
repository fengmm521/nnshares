
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import time
import urllib2
#btcc:https://data.btcchina.com/data/ticker?market=ltccny

def getUrl(purl):
    try:
        req = urllib2.Request(purl)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req)
        html = res.read()
        return html
    except Exception, e:
        print e
    return 0


def main():
    dat = getUrl('http://news.10jqka.com.cn/field/sn/20170331/9959769.shtml')
    print dat
if __name__ == '__main__':
    main()