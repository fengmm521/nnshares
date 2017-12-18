#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import json
import time

sys.path.append('..')

import DateTool

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

import tushare as ts

import shareMsgDownTool
import GongGaoTool

def downloadSharelistWithTushare(savepth):
    dat = ts.get_stock_basics()     #获取所有股票业绩
    dat.to_csv(savepth)


def getTodayShareList():
    todaynum = DateTool.getNowNumberDate()
    xlspth = '../xlsx/%s'%(str(todaynum))
    if not os.path.exists(xlspth):
        os.mkdir(xlspth)
    savepth = xlspth + os.sep + str(todaynum) + '_list.csv'
    if os.path.exists(savepth):
        print '今天股票列表已下载,不用重复下载。可直接使用:%s'%(savepth)
    else:
        print '下载今天的股票列表'
        downloadSharelistWithTushare(savepth)
    return savepth

#获取所有股票信息
def getAllShareDat():
    tmpth = getTodayShareList()
    f = open(tmpth,'r')
    lines = f.readlines()
    f.close()

    lines = lines[1:]

    shares = {}
    for l in lines:
        tmpl = l.replace('\r','')
        tmpl = tmpl.replace('\n','')
        tmps = tmpl.split(',')
        shares[tmps[0]] = tmps
    return shares

#获取所有股票ID
def getAllShareID():

    shares = getAllShareDat()
    ids = shares.keys()
    return ids


def downShareWithTID(tid,savedir,savename):

    if not os.path.exists(savedir):
        os.mkdir(savedir)

    savepth = savedir + os.sep + savename
    if os.path.exists(savepth):
        print '%s 已下载，不用重复下载'%(tid)
        return True

    sharetool = shareMsgDownTool.ShareMsgTool()
    dictmp = sharetool.companyMsg(tid)
    if not dictmp or dictmp.keys() == 0:
        print '%s 下载错误，未获得数据'
        return False
        
    # tmpstr = json.dumps(comdic,ensure_ascii=False)
    jsonstr = json.dumps(dictmp,ensure_ascii=False)
    f = open(savepth,'w')
    f.write(jsonstr)
    f.close()
    return True

def getGongGaoLastDate(pth):

    if os.path.exists(pth): 
        f = open(pth,'r')
        lines = f.readlines()
        f.close()

        dates = []
        for l in lines:
            if len(l) > 3:
                tmpdate = l.split('|')[0]
                dates.append(tmpdate)
        dates.sort(reverse = False)
        print dates[0],dates[-1]
        return dates[0]
    else:
        return None

def downShareGongGaoWithTID(tid,savedir,savename):

    if not os.path.exists(savedir):
        os.mkdir(savedir)

    savepth = savedir + os.sep + savename
    lastDate = getGongGaoLastDate(savepth)
        
    sharetool = GongGaoTool.GongGaoTool()
    datas = sharetool.companyMsg(tid,lastDate)
    if not datas:
        print '%s 未发布新公告或者未获取到数据'
        return False
        
    # tmpstr = json.dumps(comdic,ensure_ascii=False)
    outstr = ''
    for d in datas:
        outstr += d + '\n'
    outstr = outstr[:-1]
    f = open(savepth,'a')
    f.write(outstr)
    f.close()
    return True

#获取所有股票今天的信息数据
def getAllShareTodayMsg():
    if not os.path.exists('out'):
        os.mkdir('out')
        os.mkdir('out/commsg')
        os.mkdir('out/gonggao')
    todaynum = str(DateTool.getNowNumberDate())
    todaypth = 'out/commsg/' + todaynum
    if not os.path.exists(todaypth):
        os.mkdir(todaypth)

    ids = getAllShareID()
    for tid in ids:
        print '开始下载:',tid
        savedir = todaypth + os.sep + tid
        downShareWithTID(tid, savedir,'companymsg.txt')
        time.sleep(2)

def getAllShareGongGao():
    if not os.path.exists('out'):
        os.mkdir('out')
        os.mkdir('out/commsg')
        os.mkdir('out/gonggao')
    todaynum = str(DateTool.getNowNumberDate())
    todaypth = 'out/gonggao/' + todaynum
    if not os.path.exists(todaypth):
        os.mkdir(todaypth)

    ids = getAllShareID()
    for tid in ids:
        print '开始下载:',tid
        savedir = todaypth + os.sep + tid
        downShareGongGaoWithTID(tid, savedir,'gonggao.txt')
        time.sleep(2)


def main():
    
    # getAllShareTodayMsg()
    getAllShareGongGao()
    
if __name__ == '__main__':  
    main()
    