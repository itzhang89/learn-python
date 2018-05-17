# -*- coding: utf-8 -*-
"""
这是一个地址爬取程序，或者全国的行政地址信息
"""

import requests
import bs4
import os, logging.config, json
import pickle
from datetime import datetime
import pprint
import re
from functools import reduce


def setup_logging(
        default_path='logs/logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration
 
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


baseUrl = "http://www.xzqh.org/html/"
splitSep = '\u0019'
tabSep = '    '


def parseUrl(url, session=None, errorLink=set(), decodeType='gbk'):
    """
    解析url，并返回一个bs4对象,错误连接放入到errorLink集合中\n
    :param url: 解析的url\n
    :param session: 如果已经存在会话session，则使用已存在会话，否则新建一个\n
    :param errorLink: 解析出错的连接存放\n
    :param decodeType: 解码格式，默认gbk\n
    :return: 返回url解析的beatifualSoup对象\n
    """
    startUrl = baseUrl + url
    if not session:
        session = requests.Session()
        session.get(startUrl)  # 设置回话
    try:
        res = session.get(startUrl)
        res.raise_for_status
    except Exception as e:
        logging.error("connection error: <{}> {}".format(startUrl, e))
        errorLink.add(startUrl)
        return;

    html = res.text
    # 需要重新定义下编码格式，不然会出现乱码，无法正确匹配数据
    html = html.encode(encoding=res.encoding, errors='ignore').decode(decodeType, errors='ignore')
    bsObj = bs4.BeautifulSoup(html, 'lxml')

    return bsObj


# =============================================================================
# 将变量通过pickle模块，读写变量到文件中,isPrint是否输出一份格式化后的数据
# =============================================================================
def dumpVariableToFile(variable, fileName, extName='.dat', isPprint=False):
    datetimeStr = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    fileName = fileName + datetimeStr + extName
    with open(fileName, 'wb') as f:
        pickle.dump(variable, f)

    if isPprint:
        with open(fileName + ".pprint", 'w') as f:
            f.write(pprint.pformat(variable, indent=1, width=200, compact=True))


def loadVariableFromFile(fileName):
    with open(fileName, 'rb') as f:
        return pickle.load(f)


# =============================================================================
# 第一次解析出所有的Link连接，放入到resultLink中
# =============================================================================
# 排除的台湾省的链接地址
excludeLink = ["list/376.html", "list/377.html", "list/1324.html", "list/1328.html", "list/1326.html", "list/1325.html",
               "list/1327.html", "list/1329.html", "list/1330.html", "list/1331.html", "list/1332.html",
               "list/1333.html", "list/1335.html", "list/1336.html", "list/1337.html", "list/1338.html",
               "list/1341.html", "list/1342.html", "list/1343.html", "list/1344.html"]


def firstParseUrlContentTolinkList(bsObj):
    items = bsObj.select("#site_map ul li a")
    resultLink = set()
    for item in items:
        # 如果存在span标签，则跳过
        hrefLink = item.get('href')
        if item.span or hrefLink in excludeLink:
            continue
        if hrefLink:
            resultLink.add(item.get('href'))

    logging.info("first link total :%d" % len(resultLink))
    return resultLink


# =============================================================================
# 将第一次解析的连接中数据，进一步的解析出连接
# =============================================================================

# 过滤掉数据,含有下面两者的数据跳过
def filterName(nameString):
    for tem in ["概况地图", "历史沿革"]:
        if nameString.find(tem) != -1:
            return False
    return True


def secondParseUrlContentTolinkDict(bsObj):
    liItems = bsObj.select("div .text_list .text_list_f14 li")
    resultLink = list()  # 除“行政区划”的列表
    areas = list()  # “行政区划”的列表
    for item in liItems:
        aTag = item.findChild('a')
        hrefLink = aTag.get('href')
        name = aTag.get_text()
        if filterName(name):
            if name.find('行政区划') != -1:
                areas.append((name, hrefLink))
            else:
                resultLink.append((name, hrefLink))

    # 如果只有一个行政区划，则返回行政区划
    if len(areas) == 1:
        return areas[0]
    # 如果不止一个，返回最新的行政区划
    elif len(areas) > 1:
        yearDict = dict()
        for area in areas:
            tmp = re.search('(\d{4})', area[0])
            if tmp:
                yearDict[tmp.group(1)] = area
            else:
                logging.info("max is area {}".format(area))
                return area
        maxYear = max(map(lambda x: int(x), yearDict.keys()))
        logging.info("max year {}, areas: {}".format(maxYear, areas))
        return yearDict[str(maxYear)]
    # 否则返回一个列表
    else:
        return resultLink


# =============================================================================
# 解析"行政区划"中的数据代码
# =============================================================================
def parsePageLink(bsObj):
    contentTag = bsObj.find('div', class_='content')
    pages = contentTag.find('div', {'id': 'pages'}).find_all('a')
    if pages:
        pagesSet = set()
        for page in pages[1:-1]:  # 排除前后两个标签
            href = page.get('href')
            pagesSet.add(href)
        return pagesSet
    return None


def parseTupleUrlContent(bsObj):
    # 显示页面的次数
    contentTag = bsObj.find('div', class_='content')
    pages = contentTag.find('div', {'id': 'pages'}).find_all('a')
    totalTupleList, raw = ([], '')
    pageString = ''
    if pages:
        pagesSet = set()
        for page in pages[1:-1]:  # 排除前后两个标签
            href = page.get('href')
            pagesSet.add(href)

        logging.info("the url is not single {}".format(pagesSet))
        for page in pagesSet:
            suBsObj = parseUrl(page, s, errorLink)
            (subTupleList, subRaw) = getContextFromdm220(suBsObj)
            totalTupleList += subTupleList
            raw += subRaw

        for page in pagesSet:
            pageString += splitSep + page

    else:
        totalTupleList, raw = getContextFromdm220(bsObj)

    return totalTupleList, raw, pageString


def getContextFromdm220(bsObj):
    liItems = bsObj.find_all('div', class_='dm220')
    pca = parseProvinceCityArea(bsObj)  # 获取省市区前缀
    content = ''
    if len(liItems) > 0:
        for item in liItems:
            content += item.text + '\r\n'
    else:
        raw = cleanBlackWord(parseContentFrom(bsObj))
        return ([pca], raw)

    splitItems = content.split('\r\n')
    splitItems.pop()

    streetSet = set()
    communitySet = set()
    resultDict = dict()
    for item in splitItems:
        matchObj = re.match('(\d+)', item)
        if bool(matchObj):
            itemNumber = matchObj.group(1)
            itemName = re.sub('(\d+)', '', item).strip()
            if len(matchObj.group(1)) == 9:
                streetSet.add((itemNumber, itemName))
            elif len(matchObj.group(1)) == 12:
                communitySet.add((itemNumber, itemName))

    for street in streetSet:
        resultDict[street[1]] = set()
        for community in communitySet:
            if community[0].startswith(street[0]):
                resultDict[street[1]].add(community[1])

    resultList = []
    for street, communitys in resultDict.items():
        combine = ''
        for community in communitys:
            combine += splitSep + community

        combine = combine[1:] if combine else ''
        resultList.append(pca + tabSep + street + tabSep + combine)

    return (resultList, cleanBlackWord(content))


# =============================================================================
# 
# =============================================================================
def parseContentFrom(bsObj):
    item = bsObj.find('div', class_='content')

    return item.text if item else ''


def parseListUrlRoadAndCommunity(bsObj):
    pca = parseProvinceCityArea(bsObj)  # 获取省市区前缀 ,以\u0019分割
    pageString = ''
    try:
        street = bsObj.select("div #show h1").pop().string
    except:
        logging.error("the street is not exist,the address is {}" + pca)
        return (pca, cleanBlackWord(parseContentFrom(bsObj)), pageString)

    pages = parsePageLink(bsObj)
    resultData = ''

    if pages:
        for page in pages:
            suBsObj = parseUrl(page, s, errorLink)
            datas = suBsObj.select("div #show .content p")
            for data in datas:
                if re.search("((~|～)\d+)", data.text):
                    resultData += data.text + "\t"

            pageString += splitSep + page
    else:
        datas = bsObj.select("div #show .content p")
        for data in datas:
            if re.search("((~|～)\d+)", data.text):
                resultData += data.text + "\t"

    community = parseRoadCommunity(resultData)
    return (pca + tabSep + street + tabSep + community, cleanBlackWord(resultData), pageString)


def parseRoadCommunity(rawString):
    result = set()
    pattern = "[\s~～]\d{3,3}([^\d\s]{2,12})"
    rawString = re.sub("\s", ' ', rawString)
    mathObj = re.findall(pattern, rawString, re.M)
    result = ''
    for line in mathObj:
        line = re.sub('[\s~～]\d{3,3}', '', line)
        # 去除重复的元素
        if not line in result:
            result += line + splitSep

    return result[0:-1] if result else ''  # 移除最后的一个字符


# =============================================================================
# 解析第二部分提取的链接中为空，省、市、区
# =============================================================================
def parseProvinceCityArea(bsObj):
    items = bsObj.select("div .nav_show > a")
    province, city, area = '', '', ''
    if len(items) == 4:
        area = items.pop().string
        city = items.pop().string
        province = items.pop().string
    elif len(items) == 3:
        area = items.pop().string
        city = items.pop().string

    return province + tabSep + city + tabSep + area


# =============================================================================
# 清洗数据规则
# =============================================================================
# 清除空白符号
def cleanBlackWord(string):
    string = re.sub('\s', ' ', string)
    return re.sub(' +', ' ', string)


class resultData():
    def __init__(self, url, address, flag='list', raw=''):
        self.url = url
        self.flag = flag
        self.address = address
        self.raw = raw

    def getJsonData(self):
        return {"url": self.url, "flag": self.flag, "address": self.address, "raw": self.raw}


# =============================================================================
# 主函数
# =============================================================================
if __name__ == '__main__':
    # 设置日志和会话
    setup_logging()
    s = requests.Session()
    s.get(baseUrl)  # 设置回话
    errorLink = set()  # 放着各个地方出错的链接
    logging.info("start program,and start url %s" % baseUrl)
    #    # 第一个爬取网页的所有连接
    #    firstUrl = "sitemap.html"
    #    logging.info("start the process....")
    #    bsObj = parseUrl(firstUrl,s)
    #    firstResultLink = firstParseUrlContentTolinkList(bsObj)
    #
    #    # 从第一个的所有连接中解析出第二个连接

    #    secondResultDict = dict()
    #    for url in firstResultLink:
    #        bsObj = parseUrl(url,s,errorLink)
    #        secondResultDict[url] = secondParseUrlContentTolinkDict(bsObj)
    #    logging.info("second error link number {} and value {}".format(len(errorLink),errorLink))
    #    dumpVariableToFile(secondResultDict,'secondResultDict',isPprint=True)

    secondResultDict = loadVariableFromFile("secondResultDict20180121_16_08_07.dat")

    # 解析提取出来的数据
    index = 0
    totalResult = list()
    try:
        for key, value in secondResultDict.items():
            if isinstance(value, tuple):
                xzUrl = value[1]
                bsObj = parseUrl(xzUrl, s, errorLink)
                if bsObj:
                    (tupleList, raw, pages) = parseTupleUrlContent(bsObj)
                    for line in tupleList:
                        a = resultData(url=xzUrl, flag="tuple", address=line, raw=raw)
                        raw = xzUrl + pages  # 将后面的值指向index
                        totalResult.append(a.getJsonData())
                else:
                    logging.warning("the attribute is none " + xzUrl)
                    continue

            elif isinstance(value, list):
                for item in value:
                    listUrl = item[1]
                    bsObj = parseUrl(listUrl, s, errorLink)

                    if bsObj:
                        (line, raw, pages) = parseListUrlRoadAndCommunity(bsObj)
                    else:
                        raw, pages = '', ''
                        logging.warning("the attribute is none " + listUrl)

                        continue

                    a = resultData(url=listUrl + pages, flag="list", address=line, raw=raw)
                    totalResult.append(a.getJsonData())
            elif isinstance(value, None):
                valueNullUrl = key
                bsObj = parseUrl(valueNullUrl, s, errorLink)
                if bsObj:
                    line = parseProvinceCityArea(bsObj)
                    a = resultData(url=valueNullUrl, flag="null", address=line, raw='')
                    totalResult.append(a.getJsonData())
                else:
                    logging.warning("the attribute is none " + valueNullUrl)
                    continue

            index += 1
            if (index % 100) == 0:
                logging.info("have read url {}/{}, error Link number is {}".format(index, len(secondResultDict.keys()),
                                                                                   len(errorLink)))

    except KeyboardInterrupt as e:
        logging.info(e)
    finally:
        dumpVariableToFile(totalResult, 'totalResult', isPprint=True)
