from urllib import request
from bs4 import BeautifulSoup
import re


class NewsType:
    def __init__(self, name, link):
        self.name = name
        self.link = link

urlTypeMap = {
    "SDXW": NewsType("视点新闻", "https://www.cumt.edu.cn/19673"),
    "XSJJ": NewsType("学术聚焦", "https://www.cumt.edu.cn/19674"),
    "XSBG": NewsType("学术报告", "https://www.cumt.edu.cn/19676"),
    "RWJT": NewsType("人文课堂", "https://www.cumt.edu.cn/19677"),
    "XWGG": NewsType("信息公告", "https://www.cumt.edu.cn/19678"),
    "XYKX": NewsType("校园快讯", "https://www.cumt.edu.cn/19679"),
}


class News:
    def __init__(self, title, link, time):
        self.title = title
        self.link = link
        self.time = time

    def toJson(self):
        return {
            "title": self.title,
            "link": self.link,
            "date": self.time
        }


class NewsSpider:
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    def __init__(self, typeStr, page=1):
        self.type = urlTypeMap[typeStr]
        self.url = self.type.link
        self.page = page
        if self.page != 1:
            self.maxPage = self.__getMaxPage(1)
        else:
            self.maxPage = self.__getMaxPage(self.page)
        if self.page > self.maxPage:
            self.page = self.maxPage
        elif self.page < 1:
            self.page = 1
        self.html = self.__getHtml(self.page)

    # 获取网页源码
    def __getHtml(self, page):
        url = self.url + "/list" + str(page) + ".htm"
        req = request.Request(url, headers=self.header, method="GET")
        requests = request.urlopen(req)
        return requests.read().decode('utf-8')

    # 获取新闻列表
    def toJson(self):
        result = []
        soup = BeautifulSoup(self.html, 'html.parser')
        soup = soup.select('ul[class="news_list list2"]')
        soup = soup[0].select('li')
        for i in soup:
            title = i.select('a')[0].get_text()
            link = i.select('a')[0].get('href')
            time = i.select('span[class="news_meta"]')[0].get_text()
            news = News(title, link, time)
            result.append(news.toJson())
        return {
            "current_page": self.page,
            "max_page": self.maxPage,
            "type": self.type.name,
            "data": result
        }

    # 获取最大页数
    def __getMaxPage(self, page):
        html = self.__getHtml(page)
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.select('em[class="all_pages"]')
        return int(soup[0].get_text())


class ContentSection:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def toJson(self):
        return {
            "type": self.type,
            "content": self.content
        }


class ContentSpider:
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    def __init__(self, link):
        self.link = link
        self.urlHead = re.compile(r'[a-zA-z]+://[^\s]*?/').search(self.link).group()
        self.html = self.__getHtml()

    def __getHtml(self):
        req = request.Request(self.link, headers=self.header, method="GET")
        requests = request.urlopen(req)
        return requests.read().decode('utf-8')

    def toJson(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        title = soup.select('h1[class="arti_title"]')[0].getText().strip()
        temp = soup.select('div[class="news_xx"]')[0].findAll('span')
        author = temp[1].getText()
        date = temp[3].getText()
        visitCount = self._getVisitCount(temp[5].find_next().get("url"))
        contents = soup.select('div[class="wp_articlecontent"]')[0].findAll()
        contentsResult = []
        for content in contents:
            if content.name == "p":
                contentsResult.append(ContentSection("text", content.getText()).toJson())
            elif content.name == "img":
                contentsResult.append(ContentSection("image", self.urlHead[:-1] + content.get("src")).toJson())
        result = {
            "title": title,
            "author": author,
            "date": date,
            "contents": contentsResult,
            "visit_count": visitCount
        }
        return result

    def _getVisitCount(self, urlTail):
        url = self.urlHead + urlTail[1:]
        req = request.Request(url, headers={
            "Referer": self.link
        }, method="POST")
        requests = request.urlopen(req)
        result = requests.read().decode('utf-8')
        result = int(re.compile(r'\d+').search(result).group())
        return result
