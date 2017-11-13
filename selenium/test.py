#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time

import selenium.webdriver.chrome.webdriver as  wd


def main():
    browser = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')
    # browser = webdriver.phantomjs()
    browser.get('http://www.baidu.com')

    browser.find_element_by_id('kw').send_keys('selenium')
    browser.find_element_by_id('su').click()

    # browser.quit()

    str = raw_input("input any key to end: ")  #raw_input()函数读取的是键盘上输入的字符串
    # str = input("Enter your input: ");       #input()函数可以读取一个字符串


#测试
if __name__ == '__main__':
    main()




