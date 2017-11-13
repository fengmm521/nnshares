#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time

import selenium.webdriver.chrome.webdriver as  wd


def main():

    datas = {}

    browser = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')
    # browser = webdriver.phantomjs()
    browser.get('http://basic.10jqka.com.cn/300715/company.html')

    # tabtext = browser.find_element_by_xpath("//div[@id=’manager’ and @stat='company_manager']")
    manger = browser.find_element_by_id('manager')
    hd = manger.find_element_by_class_name('hd')
    bd = manger.find_element_by_class_name('bd')

    print hd.text
    # browser.find_element_by_id('kw').send_keys('selenium')
    # browser.find_element_by_id('su').click()
    bddsh = bd.find_element_by_name('ml_001')                       #董事会菜单

    print '董事会菜单:',bddsh.text

    bdjsh = bd.find_element_by_name('ml_002')                       #监事会菜单

    print '监事会菜单:',bdjsh.text

    bdgg = bd.find_element_by_name('ml_003')                        #高管菜单

    print '高管菜单:',bdgg.text
    bddshcy = bd.find_element_by_id('ml_001')                       #董事会成员列表,注意这个是by_id

    print '董事会成员',bddshcy.text
    turnto = bddshcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = bddshcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['dsh'] = dattmps

    time.sleep(0.1)

    bdjsh.click()               #点击打开监事会列表

    time.sleep(0.1)

    bdjshcy = bd.find_element_by_id('ml_002')                   #监事会成员列表,by_id

    print '监事会成员:',bdjshcy.text
    turnto = bdjshcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = bdjshcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['jsh'] = dattmps

    bdgg.click()                #打开高管列表
    time.sleep(0.1)

    ggcy = bd.find_element_by_id('ml_003')                  #高管列表,by_id

    print '高管成员:',ggcy.text
    turnto = ggcy.find_elements_by_class_name('turnto')         #成员名列表
    hidds = ggcy.find_elements_by_class_name('person_table')     #发现person列表数组

    dattmps = []
    for n in range(len(turnto)):
        turnto[n].click()                                          #打开成员详情
        h = hidds[n]                                                #获取详情内容
        clo = h.find_element_by_class_name('close')                 #关闭按钮
        dattmps.append(h.text)                                      #保存详情
        clo.click()                                                 #关闭当前详情

    datas['gg'] = dattmps

    # browser.quit()
    
    browser.quit()

    str = raw_input("input any key to end: ")  #raw_input()函数读取的是键盘上输入的字符串
    # str = input("Enter your input: ");       #input()函数可以读取一个字符串

    for k in datas.keys():
        dat = datas[k]
        for d in dat:
            print d
        str = raw_input("input any key to end: ")  #raw_input()函数读取的是键盘上输入的字符串
    


#测试
if __name__ == '__main__':
    main()




