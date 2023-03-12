from urllib import request
from bs4 import BeautifulSoup
import re


# 新闻类型
class NewsType:
    def __init__(self, name, link):
        self.name = name
        self.link = link


typeMap = {
    "SDXW": NewsType("视点新闻", "https://www.cumt.edu.cn/19673"),
    "XSJJ": NewsType("学术聚焦", "https://www.cumt.edu.cn/19674"),
    "XSBG": NewsType("学术报告", "https://www.cumt.edu.cn/19676"),
    "RWJT": NewsType("人文课堂", "https://www.cumt.edu.cn/19677"),
    "XWGG": NewsType("信息公告", "https://www.cumt.edu.cn/19678"),
    "XYKX": NewsType("校园快讯", "https://www.cumt.edu.cn/19679"),
}


# 新闻列表项
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


# 新闻列表爬虫
class NewsSpider:
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    def __init__(self, typeStr, page=1):
        self.type = typeMap[typeStr]
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
            link = self.__genLink(i.select('a')[0].get('href'))
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

    def __genLink(self, link):
        if link.startswith("http"):
            return link
        else:
            return "https://www.cumt.edu.cn" + link


# 新闻内容单个段落
class ContentParagraph:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def toJson(self):
        return {
            "type": self.type,
            "content": self.content
        }


# 新闻内容
class NewsContent:
    def __init__(self, title, author, date, contents, visitCount):
        self.title = title
        self.author = author
        self.date = date
        self.content = contents
        self.visitCount = visitCount

    def toJson(self):
        return {
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "contents": self.content,
            "visit_count": self.visitCount
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
        result = NewsContent("", "", "", [], 0).toJson()
        result = self.__normalPageToJson(soup)
        if result is None:
            result = self.__pdfPageToJson(soup)
        return result

    def __normalPageToJson(self, soup):
        try:
            title = soup.select('h1[class="arti_title"]')[0].getText().strip()
            temp = soup.select('div[class="news_xx"]')[0].findAll('span')
            author = temp[1].getText()
            date = temp[3].getText()
            visitCount = self._getVisitCount(temp[5].find_next().get("url"))
            contents = soup.select('div[class="wp_articlecontent"]')[0]
            contentsResult = self.__analyticalParagraph(contents)
            result = NewsContent(title, author, date, contentsResult, visitCount).toJson()
            return result
        except Exception as e:
            print(e)
            return None

    # 解析pdf段落
    def __analyticalPdfParagraph(self, soup):
        pdfUrlTail = soup.get("pdfsrc")[1:]
        pdfUrl = self.urlHead + pdfUrlTail
        return ContentParagraph("pdf", pdfUrl).toJson()

    # 平行遍历标签，解析每一段
    def __analyticalParagraph(self, soup):
        contentsResult = []
        for content in soup.children:
            try:
                if content.name is None:
                    continue
                elif content.name == "p":
                    if content.next.name == "img":
                        contentsResult.append(
                            ContentParagraph("image", self.urlHead[:-1] + content.next.get("src")).toJson())
                    elif content.find_all('div'):
                        contentsResult.append(
                            self.__analyticalPdfParagraph(content.find_all('div')[0]))
                    else:
                        contentsResult.append(ContentParagraph("text", content.getText()).toJson())
                elif content.name == "div":
                    contentsResult.append(self.__analyticalPdfParagraph(content))

                else:
                    contentsResult.append(
                        ContentParagraph("text", "未解析段落类型：" + content.name).toJson())
            except Exception as e:
                print(e)
                contentsResult.append(ContentParagraph("text", "[该段落解析失败]").toJson())
        return contentsResult

    def __pdfPageToJson(self, soup):
        try:
            title = soup.select('h1[class="arti_title"]')[0].getText().strip()
            author = soup.select('span[class="arti_publisher"]')[0].getText().split("：")[1]
            date = soup.select('span[class="arti_update"]')[0].getText().split("：")[1]
            visitCount = self._getVisitCount(soup.select('span[class="WP_VisitCount"]')[0].get("url"))
            contents = soup.select('div[class="wp_articlecontent"]')[0]
            contentsResult = self.__analyticalParagraph(contents)
            result = NewsContent(title, author, date, contentsResult, visitCount).toJson()
            return result
        except Exception as e:
            print(e)
            return None

    def _getVisitCount(self, urlTail):
        url = self.urlHead + urlTail[1:]
        req = request.Request(url, headers={
            "Referer": self.link
        }, method="POST")
        requests = request.urlopen(req)
        result = requests.read().decode('utf-8')
        result = int(re.compile(r'\d+').search(result).group())
        return result