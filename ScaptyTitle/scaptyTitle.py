# -*- coding: utf-8 -*-
# Describe:用来爬取网页中文档和作者名
# Author:jhzhang
# Data:2018/5/17

import json
import logging.config
import os
from datetime import datetime

import ScratchUtils as Utils
import bs4
import requests

baseUrl = "http://www.my285.com/"
dateStr = datetime.now().strftime("%Y%m%d")


def parseUrl(url, session=None, errorLink=set(), decodeType='gbk'):
    if not session:
        s = requests.Session()
        s.get(url)  # 设置回话
    s = session
    try:
        res = s.get(url)
        res.raise_for_status
    except Exception as e:
        logging.error("connection error: <{}> {}".format(url, e))
        errorLink.add(url)
        return

    html = res.text
    # 需要重新定义下编码格式，不然会出现乱码，无法正确匹配数据
    html = html.encode(encoding=res.encoding, errors='ignore').decode(decodeType, errors='ignore')
    bsObj = bs4.BeautifulSoup(html, 'lxml')
    return bsObj


def parseFullUrl(url, rule, session=None, decodeType='gbk'):
    """
    根据url和规则解析返回的数据
    :param url:
    :param rule:
    :param session:
    :param decodeType:
    :return:
    """
    if not session:
        session = requests.Session()
        session.get(url)  # 设置回话
    try:
        res = session.get(url)
        res.raise_for_status
    except Exception as e:
        logging.error("connection error: <{}> {}".format(url, e))
        return None

    html = res.text
    # 需要重新定义下编码格式，不然会出现乱码，无法正确匹配数据
    html = html.encode(encoding=res.encoding, errors='ignore').decode(decodeType, errors='ignore')
    bsObj = bs4.BeautifulSoup(html, 'lxml')
    return bsObj.select(rule)


def parseAuthorUrlFile(fileStr, session=None, errorLink=set()):
    """
    输入的是链接和规则，例如，url\trule，返回字典列表

    :param fileStr: 存储的文件
    """
    result = list()
    for line in parseFileToList(fileStr):
        line = line.strip()
        [url, rule] = str(line).split("\t")
        logging.info("开始解析url 「%s」和规则「%s」", url, rule)
        obj = parseUrl(baseUrl + url, session, errorLink)
        if not obj:
            logging.info("the url 「%s」 and 「rule」 %s is parse error", baseUrl + url, rule)
        # 去掉前后的引号
        rule = rule[1:-1]
        links = obj.select(rule)
        for i in links:
            author = i.get_text().strip()
            titleUrl = i.get("href").strip()
            authorDict = dict()
            authorDict["author"] = author
            authorDict["sortUrl"] = url
            authorDict["titleUrl"] = titleUrl
            result.append(authorDict)

    if errorLink.__len__() > 0:
        logging.info("存在未获取的数据 errorLink")
        Utils.dumpVariableToFile(errorLink, "AuthorErrorLink", isPprint=True)

    if len(result) > 0:
        logging.info("写入爬取到的作者和连接")
        Utils.dumpVariableToFile(result, "authorUrlList", isPprint=True)
    return result


def parseFileToList(fileStr, result=[]):
    """
    输入文件名，返回文件列表（适用于文件量不大的情况），后期可以改为迭代器

    :param result:
    :param fileStr: 输入的解析文件路径
    :param Lists: 返回的结果
    """
    if not os.path.exists(fileStr):
        logging.error("your input file path ‘%s’ isn't exist", fileStr)

    with open(fileStr, 'r', encoding='utf-8') as f:
        for line in f:
            if line.lstrip().startswith("#"):
                continue
            if line.strip():
                result.append(line)

    return result


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
                except:
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


class Author(object):
    def __init__(self, name, url, rule=None, tities=[]):
        self.name = name
        self.url = url
        self.titleList = tities
        self.rule = rule

    def __str__(self):
        return str(self.__dict__)


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
    # def default(self, obj):
    #     if isinstance(obj, dict):
    #         return [obj.real, obj.imag]
    #     # Let the base class default method raise the TypeError
    #     return json.JSONEncoder.default(self, obj)


def parseTitleUrls():
    authorFullUrlList = Utils.loadVariableFromFile("./authorFullUrlList20180519_10_46_46.dat")
    authorFullUrlTitleList = []
    rule = "td[bgcolor='#FFFFFF'] a[href]"
    # 记录所有的文章链接和规则
    titles = []
    for line in authorFullUrlList:
        titlesUrl = line["url"]
        titleItems = parseFullUrl(titlesUrl, rule)
        # 解析出多篇文章的url
        for item in titleItems:
            titleName = item.text
            titleUrl = item.get("href")
            if not titleName or not titleUrl:
                continue
            try:
                url = mergeUrl(titlesUrl, titleUrl)
                title = Title(line["author"], titleName, url)
                titles.append(title)
                print(title)
            except:
                logging.info("文档总连接 {%s}， 文章链接 {%s} 无法解析", titlesUrl, item)
                continue
    Utils.dumpVariableToFile(titles, "titles")
    return titles


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


def parseTitleUrl(titleObj, errorList=[], session=None, defaultRule=None):
    """
    输入一个Title类，并且写入规则
    :param titleObj:
    :param errorList: 输错文件写入列表
    :param defaultRule: 默认的解析规则，如果不想启用就设置为None
    :param session: 自定义的类
    :return: 返回重新生成后的数据
    """

    if type(titleObj) == dict or type(titleObj) == str:
        titleObj = Title.valueOf(titleObj)

    if type(titleObj) == Title:
        titleName = titleObj.titleName
        author = titleObj.author
        titleUrl = titleObj.url
        rule = titleObj.rule
    else:
        return None
    # 如果没有规则，则使用默认规则，如果规则为空，则返回
    if not rule:
        rule = defaultRule
    if not rule:
        return None

    bsObj = parseFullUrl(titleUrl, rule, session)
    # 如果解析的连接没有内容，则写入错误文件fp
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
            except:
                logging.info("解析文章出错parseTitle, 作者文章链接 {%s} , 章节链接 {%s} 无法解析", titleUrl, chapterUrl)
                continue
            tmp = getSinglePageText(url, session)
            if tmp:
                text += tmp

    titleObj.title = True
    # 写入到文件中
    writeToFile(author, titleName, text, "./titles/" + dateStr)
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


def getSinglePageText(url, session=None):
    """
获得单页的文章信息
    :param url:
    :return:
    """
    rule = "tr > td[colspan='2']"
    bsObj = parseFullUrl(url, rule, session)
    for item in bsObj:
        if len(item.find_all("br")) > 3:
            return item.text
    return None


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
            except:
                continue
    return result


if __name__ == "__main__":
    Utils.setup_logging()
    session = requests.Session()
    session.get(baseUrl)  # 设置回话
    # authorUrl = "./Links/startUrl.txt"
    # authorUrlList = parseAuthorUrlFile(authorUrl)
    # 获得所有作者的相对路径路径
    # authorUrlList = Utils.loadVariableFromFile("./authorUrlList20180518_14_55_37.dat")
    # 将所有作者的信息转化为绝对路径
    # authorFullUrlList = []
    # for line in authorUrlList:
    #     url = mergeUrl(baseUrl, line["sortUrl"], line["titleUrl"])
    #     print(url)
    # cdicts = dict()
    # cdicts["author"] = line["author"]
    # cdicts["url"] = url
    # authorFullUrlList.append(cdicts)
    # 解析所有的文章列表url
    # parseTitleUrls()
    logging.info("---------解析所有文章的内容-------")
    # titles = Utils.loadVariableFromFile("./titles20180521_08_50_59.dat")
    titles = loadVariableFromJson("./titles20180523_09_14_25.json")
    parseTitle(titles, session)
    dumpVariableToJson(titles, "titles")
    logging.info("--------over----------")
