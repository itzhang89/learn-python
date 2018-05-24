# PythonLearn
记录一些学习Python的语法知识和心得，并且利用Python实现的网络爬虫



## 爬取网络上的文章

- [ ] 爬取“[梦远书城](http://www.my285.com/xdmj/index.htm)”中的「[现代文学]((http://www.my285.com/xdmj/index.htm))」、「[言情小说](http://www.my285.com/yq/index.htm)」、「[武侠小说](http://www.my285.com/wuxia/index.htm)」，获取每个作者信息和对应的url
- [ ] 解析每个作者的Url和爬取作者名下文章



### 获取链接：

通过配置:

> ```
> wuxia/index.htm "body td.bg > a[href]"
> yq/index.htm   "body td.t3 > a[href]"
> xdmj/index.htm "body td[bgcolor="#FFFFFF"] > a[href]"
> ```



### 第一次爬取

---

2018/5/23 星期三

存储在20180523_103410.tar.gz 文件中，爬取失败

250行，{'author': '黄易', 'titleName': '魔女殿', 'url': 'http://www.my285.com/wuxia/huangyi/006.htm', 'rule': None, 'title': None}失败

- 主要原因，是该链接是小短文，缺少数据



### 第二次爬取

2018/5/23 星期三

从前面250行开始爬取。

### 第三次大量爬取

2018/5/23 星期三

重新的整理了部分地址数据信息

1. 分析了地址中的主要链接有如下的特点
   1. 以 index.htm结尾的链接通常表示长篇小说
   2. 以00*.htm结尾的链接通常表示短片文章