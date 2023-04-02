# 矿大官网新闻 后端
## 使用方法
### 1. 安装依赖
```bash
pip install -r requirements.txt
```
### 2. 运行
运行`app.py`的`main`函数即可启动服务。
### 3. 测试
将项目目录下的`cumt_spider.postman.json`导入到Postman，即可测试接口。
## API
### 1. 获取新闻类型
- 方法：GET
- 接口：http://127.0.0.1:5000/news/type
#### Response
```json
{
    "data": [
        {
            "link": "https://www.cumt.edu.cn/19673",
            "name": "视点新闻",
            "type": "SDXW"
        },
        {
            "link": "https://www.cumt.edu.cn/19674",
            "name": "学术聚焦",
            "type": "XSJJ"
        },
        {
            "link": "https://www.cumt.edu.cn/19676",
            "name": "学术报告",
            "type": "XSBG"
        },
        {
            "link": "https://www.cumt.edu.cn/19677",
            "name": "人文课堂",
            "type": "RWJT"
        },
        {
            "link": "https://www.cumt.edu.cn/19678",
            "name": "信息公告",
            "type": "XWGG"
        },
        {
            "link": "https://www.cumt.edu.cn/19679",
            "name": "校园快讯",
            "type": "XYKX"
        }
    ]
}
```
### 2. 获取新闻列表
- 方法：GET
- 接口：http://127.0.0.1:5000/news/list
- 参数：
    - type: 新闻类型(string)，从接口1获取
    - page: 页码(int)

#### Response
```json
{
    "current_page": 1,
    "data": [
        {
            "date": "2023-03-07",
            "link": "https://xwzx.cumt.edu.cn/c8/28/c513a641064/page.htm",
            "title": "化工学院俞和胜教授指导孙越崎学院本科生在光催化降解选矿废水领域取得新进展"
        },
        {
            "date": "2023-02-27",
            "link": "https://xwzx.cumt.edu.cn/c6/59/c513a640601/page.htm",
            "title": "国家重点研发计划项目“煤与共伴生战略性金属矿产协调开采理论与技术”2022年度进展研讨会召开"
        }
    ],
    "max_page": 32,
    "type": "学术聚焦"
}

```

### 3. 获取新闻详情
- 方法：GET
- 接口：http://127.0.0.1:5000/news/content
- 参数：
    - link: 新闻链接(string)，从接口2获取
#### Response
```json
{
    "author": "李居铭",
    "contents": [
        {
            "content": "为深入贯彻落实习近平生态文明思想，让全校师生在绿色校园中体悟自然之美、劳动之美，3月10日下午，我校在南湖校区开展以“春意盎然万物新，植树护绿我先行”为主题的师生义务植树活动。在校校领导、党政机关干部代表、校级学生组织成员、校青马工程学员、第25届研究生支教团志愿者等共200余名师生一起参加了活动。",
            "type": "text"
        },
        {
            "content": "https://xwzx.cumt.edu.cn/_upload/article/images/f4/b1/ccbc653c4480a6dd04fa34e18894/13af0f94-65e1-49f1-9f2c-880e3e51f833.png",
            "type": "image"
        },
        {
            "content": "https://www.cumt.edu.cn/_upload/article/files/93/65/cb21d1e84aadb712d01071311a1b/c56d9edc-b256-4980-a404-cecafc5045f3.pdf",
            "type": "pdf"
        }
    ],
    "date": "2023-03-07",
    "title": "化工学院俞和胜教授指导孙越崎学院本科生在光催化降解选矿废水领域取得新进展",
    "visit_count": 1607
}
```
> 段落类型一共三种：text、image、pdf
