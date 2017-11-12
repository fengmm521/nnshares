#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

import tushare as ts

def main():
    dat = ts.get_stock_basics()     #获取所有股票业绩
    dat.to_csv('sharelist.csv')
if __name__ == '__main__':  
    main()
    