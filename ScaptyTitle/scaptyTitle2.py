# -*- coding: utf-8 -*-
# Describe:用来爬取网页中文档和作者名
# Author:jhzhang
# Data:2018/5/17

import json
import logging.config
import os
import re
from datetime import datetime

import ScratchUtils as Utils
import bs4
import requests

startUrl = "http://www.my285.com/"
nowDataStr = datetime.now().strftime("%Y%m%d")


def parseFullUrl(url, rule, session=None, decodeType='gbk'):
    """
    根据url和规则解析返回的数据
    :param url:
    :param rule:
    :param session:
    :param decodeType:
    :return:
    """
    try:
        res = session.get(url)
        res.raise_for_status()
    except Exception as e:
        logging.error("connection error: <{}> {}".format(url, e))
        return None

    html = res.text
    # 需要重新定义下编码格式，不然会出现乱码，无法正确匹配数据
    html = html.encode(encoding=res.encoding, errors='ignore').decode(decodeType, errors='ignore')
    bsObj = bs4.BeautifulSoup(html, 'lxml')
    return bsObj.select(rule)


def mergeUrl(baseUrl, *kwargs):
    """
    组装出URL
    :param baseUrl: 基础的Url，起始网站
    :param kwargs: 各类相对路径网址
    :return: 最终的绝对路径
    """
    urlItems = []
    if baseUrl.endswith("/"):
        baseUrl = baseUrl[0:-1]
    if baseUrl.endswith("index.htm"):
        baseUrl = baseUrl.replace("/index.htm", "")
    urlItems.append(baseUrl)
    for arg in kwargs:
        for item in arg.split("/"):
            item = item.strip()
            if not item or ".htm" in item or ".html" in item:
                continue

            if item == "..":
                try:
                    urlItems.pop()
                except Exception:
                    logging.info("解析地址出错 baseUrl: {} {}".format(baseUrl, kwargs))
                    pass
            else:
                urlItems.append(item)
    argLen = len(kwargs)
    if argLen >= 1:
        lastItem = kwargs[argLen - 1].split("/")[-1]
    else:
        lastItem = "index.html"
    urlItems.append(lastItem)
    return "/".join(urlItems)


class Title(json.JSONEncoder):
    def __init__(self, author, titleName, url, rule=None, title=None):
        self.author = author
        self.titleName = titleName
        self.url = url
        self.rule = rule
        self.title = title

    def __str__(self):
        return str(self.__dict__)

    def valueOf(dictStr):
        # 如果是字符串，转换为字典
        if type(dictStr) == str:
            try:
                dictStr = eval(dictStr)
            except:
                return None

        if type(dictStr) == dict:
            titleName = dictStr["titleName"]
            author = dictStr["author"]
            titleUrl = dictStr["url"]
            if not (titleName and author and titleUrl):
                return None

            rule = dictStr["rule"]
            title = dictStr["title"]
            return Title(author, titleName, titleUrl, rule, title)


def parseTitle(titles, session=None):
    count = 0
    # 存入错误列表
    errorList = []
    # 存入已经爬取的数据
    captes = []
    Rules = ["td[bgcolor='#EEF8FF'] a[href]", "td[bgcolor='#FFFFFF'] a[href]"]
    result = None
    count = 0
    for title in titles:
        count += 1
        if count % 10:
            logging.info("已经打印了 %d 行", count)
        try:
            for rule in Rules:
                result = parseTitleUrl(title, errorList, session, rule)
                if result:
                    captes.append(result)
                    break
        except Exception as e:
            logging.info("msg: %s, 打印到了 %d 行", e, count)

    logging.info("链接打印结束，打印到了 %d 行", count)
    dumpVariableToJson(errorList, "errorList")
    dumpVariableToJson(captes, "rightTitle")


def parseTitleUrl(titleObj, errorList=None, session=None, defaultRule=None):
    """
    输入一个Title类，并且写入规则
    :param titleObj:
    :param errorList: 输错文件写入列表
    :param defaultRule: 默认的解析规则，如果不想启用就设置为None
    :param session: 自定义的类
    :return: 返回重新生成后的数据
    """

    if errorList is None:
        errorList = []
    if type(titleObj) == dict or type(titleObj) == str:
        titleObj = Title.valueOf(titleObj)

    if not type(titleObj) == Title:
        return None
    # 如果没有规则，则使用默认规则，如果规则为空，则返回
    rule = titleObj.rule
    titleUrl = titleObj.url

    if not titleObj.rule:
        rule = defaultRule
    if not titleObj.rule:
        return None

    # 将文章地址进行分类
    if str(titleUrl).endswith("index.htm"):
        return parseMulitPageUrl(titleObj, session, rule, errorList)
    else:
        chapterName, titleContext = getSinglePageText(titleUrl, session)
        if titleContext:
            if not chapterName:
                chapterName = titleObj.titleName
            else:
                chapterName = chapterName.replace(" ", "")
            parentPath = "./titles/" + nowDataStr + "/" + titleObj.author
            writeToFile(titleObj.author, chapterName, titleContext, parentPath)
            titleObj.title = True
        else:
            errorList.append(titleObj)
            titleObj.title = False

    return titleObj


def parseMulitPageUrl(titleObj, session, rule, errorList):
    """解析多页面的链接

    :param titleObj: 输入Title对象
    :param session: 会话
    :param rule: 规则
    :param errorList: 错误链表
    :return: 返回更改后的titleObj
    """
    if not type(titleObj) == Title:
        logging.info("输入的不是Title类型")
        return None

    titleUrl = titleObj.url
    bsObj = parseFullUrl(titleUrl, rule, session)
    # 如果解析的连接没有内容，则写入错误列表
    if not bsObj:
        titleObj.title = False
        errorList.append(titleObj)
        return None
    # text记录整片文章的所有内容
    text = ""
    for item in bsObj:
        chapterUrl = item.get("href")
        if chapterUrl:
            try:
                url = mergeUrl(titleUrl, chapterUrl)
                # print(url)
            except Exception:
                logging.info("解析文章出错parseTitle, 作者文章链接 {%s} , 章节链接 {%s} 无法解析", titleUrl, chapterUrl)
                continue
            chapterName, titleContext = getSinglePageText(url, session)
            if chapterName and titleContext:
                chapterName = chapterName.replace(" ", "")
                parentPath = "./titles/" + nowDataStr + "/" + titleObj.author
                writeToFile(titleObj.author, titleObj.titleName + "_" + chapterName, titleContext, parentPath)

    titleObj.title = True
    # 写入到文件中
    return titleObj


def writeToFile(authorName, titleName, context, parentFilePath):
    if not os.path.exists(parentFilePath):
        os.mkdir(parentFilePath)

    if os.path.isdir(parentFilePath):
        try:
            with open(parentFilePath + "/" + authorName + "_" + titleName, 'w', encoding='utf-8') as f:
                f.write(context + '\n')
        except:
            logging.info("路径<%s> 下文件 %s_%s 写入失败,", parentFilePath, authorName, titleName)
    else:
        logging.error("input path <%s> not dir, failed", parentFilePath)


def getSinglePageText(url, session):
    titleName, titleText = getSinglePageTitileAndContext(url, session)
    if not titleName and not titleText:
        titleName, titleText = getSinglePageTitileAndContext1(url, session)
    return titleName, titleText


def getSinglePageTitileAndContext(url, session=None):
    """解析单个网页的文件名和内容

    :param url: 输入获取的连接Url
    :param session: 会话
    :return: 返回 （文章名，文章内容）的元祖
    """
    textRule = "tr > td[colspan='2']"
    bsObj = parseFullUrl(url, textRule, session)
    titleName = None
    titleContent = None
    # 文章名不符合的正则表达式
    notTitlePattern = "(my285)|(com)|(上一页)|(回目录)|(回首页)|(下一页)"
    for item in bsObj:
        # print(item)
        # print("--------------")
        if len(item.find_all("br")) > 5:
            titleContent = item.text
        else:
            if item.text.strip():
                m = re.search(notTitlePattern, item.text)
                if not m:
                    titleName = item.text.strip()

    return titleName, titleContent


def getSinglePageTitileAndContext1(url, session=None):
    """解析单个网页的文件名和内容

    :param url: 输入获取的连接Url
    :param session: 会话
    :return: 返回 （文章名，文章内容）的元祖
    """

    # 解析文章名
    titleRule = "tr > td center > b"
    titleName = None
    bsObj = parseFullUrl(url, titleRule, session)
    if bsObj:
        titleName = bsObj[0].text

    # 解析内容
    contextRule = "tr > td > p"
    titleContent = None
    bsObj = parseFullUrl(url, contextRule, session)
    # 文章名不符合的正则表达式
    for item in bsObj:
        # print(item)
        # print("--------------")
        if len(item.find_all("br")) > 5:
            titleContent = item.text

    return titleName, titleContent


def dumpVariableToJson(variable, fileName, extName='.json'):
    if not variable:
        return
    datetimeStr = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    fileName = fileName + datetimeStr + extName
    with open(fileName, 'w', encoding='utf-8') as f:
        for var in variable:
            f.write(str(var) + "\n")


def loadVariableFromJson(fileName, encoding='utf-8'):
    result = []
    if not os.path.exists(fileName) or not os.path.isfile(fileName):
        logging.info("文件路径 <%s> 不存在或者不是文件名", fileName)
        return result
    with open(fileName, 'r', encoding=encoding) as f:
        for line in f:
            try:
                tmpJson = eval(line)
                result.append(tmpJson)
            except Exception:
                continue
    return result


if __name__ == "__main__":
    Utils.setup_logging()
    session = requests.Session()
    session.get(startUrl)  # 设置回话
    # logging.info("---------解析所有文章的内容-------")
    # titles = loadVariableFromJson("./titles20180523_09_14_25.json")
    # parseTitle(titles, session)
    # # dumpVariableToJson(titles, "titles")
    # logging.info("--------over----------")
    titleStr = "{'author': '金庸', 'titleName': '射雕英雄传', 'url': 'http://www.my285.com/wuxia/jinyong/sdyxz/index.htm', 'rule': None, 'title': None}"
    titleObj = Title.valueOf(titleStr)

    session = requests.Session()
    session.get(titleObj.url)  # 设置回话
    rule = "td[bgcolor='#FFFFFF'] a[href]"
    errorList = []
    titleObj = parseMulitPageUrl(titleObj, session, rule, errorList=errorList)
    print(errorList)
