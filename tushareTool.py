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

import time



def getAllShareListWithToday(todaydate,isfirst = True):

    if not isfirst:
        print '等待5秒后开始下载今天股票列表'
        time.sleep(5)

    xldir = 'xlsx/' + str(todaydate)

    if not os.path.exists(xldir):
        os.mkdir(xldir)

    savepth = xldir + '/tusharedat.csv'


    if os.path.exists(savepth):
        print '%s股票列表已下载。保存在:%s'%(str(todaydate),savepth)
    else:
        print '今天股票列表未下载，正在下载。。。。'
        dat = ts.get_stock_basics()     #获取所有股票业绩
        dat.to_csv(savepth)
        print '今天股票列表下载完成，保存在:%s'(savepth)


def getShareGaiNian(todaydate,isfirst = False):

    if not isfirst:
        print '等待5秒后开始下载今天股票概念数据列表'
        time.sleep(5)

    savepth = xldir + '/gainian.csv'

    if os.path.exists(savepth):
        print '%s股票概念列表已下载，保存在:%s'%(str(todaydate),savepth)
    else:
        print '正在下载今天的股票概念列表。。。。'
        gndat = ts.get_concept_classified()
        gndat.to_csv()
        print '今天股票概念已下载完成，保存在:%s'%(savepth)

def main():
    #shutil.rmtree(dbDir)#删除目录下所有文件
    # dat = ts.get_hist_data('600848')
    # dat = ts.get_h_data('002337', autype='hfq') #后复权
    # dat = ts.get_industry_classified()            #获取行业分类


    todaydate = DateTool.getNowNumberDate()
    print todaydate

    getAllShareListWithToday(todaydate)

    getShareGaiNian(todaydate)


if __name__ == '__main__':  
    main()
    