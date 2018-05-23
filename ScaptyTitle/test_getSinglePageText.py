# -*- coding: utf-8 -*-
# Describe:
# Author:jhzhang
# Data:2018/5/23
from unittest import TestCase

import requests
import scaptyTitle2 as s2


class TestGetSinglePageTitileAndContext(TestCase):
    def test_getSinglePageTitileAndContext(self):
        # 测试长篇小说采集
        url = "http://www.my285.com/wuxia/huangyi/wjxj/04.htm"
        session = requests.Session()
        session.get(url)  # 设置回话
        titleName, titleText = s2.getSinglePageTitileAndContext(url, session)
        self.assertEqual(titleName, '第一章 武学天才(4)')
        self.assertFalse(not titleText)

    def test_getSinglePageTitileAndContext1(self):
        # 测试短片小说采集
        url = "http://www.my285.com/wuxia/huangyi/010.htm"
        session = requests.Session()
        session.get(url)  # 设置回话
        titleName, titleText = s2.getSinglePageTitileAndContext1(url, session)
        self.assertEqual(titleName, '最后战士')
        self.assertFalse(not titleText)

    # todo 这个代码没有设计好，难以测试
    def test_parseMulitPageUrl(self):
        titleStr = "{'author': '金庸', 'titleName': '射雕英雄传', 'url': 'http://www.my285.com/wuxia/jinyong/sdyxz/index.htm', 'rule': None, 'title': None}"
        titleObj = s2.Title.valueOf(titleStr)
        session = requests.Session()
        session.get(titleObj.url)  # 设置回话
        rule = "td[bgcolor='#FFFFFF'] a[href]"
        errorList = []
        titleObj = s2.parseMulitPageUrl(titleObj, session, rule, errorList=errorList)
        print(errorList)
