#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import time



def savePID(starttid):
    tmp = starttid.replace('\n')
    f = open('rpid.txt','a')
    f.write(tmp)
    f.close()
if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        starttid = args[1]
        print 'savePID:%s'%(starttid)
        savePID(starttid)
    else:
        print '保存进程ID错误,没有输入进程ID参数'