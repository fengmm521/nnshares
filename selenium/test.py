#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import time

# a = '/a/b/c/d/e/a.txt'
# print os.path.split(a)


def main(starttid):
    while True:
        print 'test startid:%s  at %s'%(starttid,time.ctime())
        time.sleep(10)
    
if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        starttid = args[1]
        print 'start from tid:%s'%(starttid)
        main(starttid)
    else:
        main()