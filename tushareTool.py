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

import DateTool


def main():
    #shutil.rmtree(dbDir)#删除目录下所有文件
    # dat = ts.get_hist_data('600848')
    # dat = ts.get_h_data('002337', autype='hfq') #后复权
    # dat = ts.get_industry_classified()            #获取行业分类


    todaydate = DateTool.getNowNumberDate()
    print todaydate

    xldir = 'xlsx/' + str(todaydate)

    if os.path.exists(xldir):
        print 'today xlsx has downloaded,today date:%s'%(str(todaydate))
    else:
        os.mkdir(xldir)

    savepth = xldir + '/tusharedat.xlsx'
    dat = ts.get_stock_basics()     #获取所有股票业绩
    dat.to_excel(savepth)

    print 'download today xlsx data is ok:%s'%(savepth)
if __name__ == '__main__':  
    main()
    