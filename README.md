# 矿大官网新闻 后端
## 使用方法
### 1. 安装依赖
```bash
pip install -r requirements.txt
```
### 2. 运行
```bash
flask run
```
### 3. 测试
将项目目录下的`postman_collection.json`导入到Postman，即可测试接口。
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
        },
      ......
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
            "content": "",
            "type": "text"
        },
        {
            "content": "https://xwzx.cumt.edu.cn/_upload/article/images/f4/b1/ccbc653c4480a6dd04fa34e18894/13af0f94-65e1-49f1-9f2c-880e3e51f833.png",
            "type": "image"
        },
        {
            "content": "近日，我校化工学院俞和胜教授指导孙越崎学院本科生沈明威在连续流光催化降解选矿废水领域取得新进展，成果以论文“Visible-light-driven photodegradation of xanthate in a continuous fixed-bed photoreactor: Experimental study and modeling”发表于化工领域国际顶级期刊《Chemical Engineering Journal》。该期刊2021年影响因子达16.744，位于中科院一区（基础版和升级版）TOP期刊、JCR一区。我校孙越崎学院2020级本科生沈明威为该成果第一作者，化工学院俞和胜教授为独立通讯作者，中国矿业大学为唯一通讯单位。",
            "type": "text"
        },
      ..........
    ],
    "date": "2023-03-07",
    "title": "化工学院俞和胜教授指导孙越崎学院本科生在光催化降解选矿废水领域取得新进展",
    "visit_count": 1607
}
```