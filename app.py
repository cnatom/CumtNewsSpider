from flask import Flask, request, jsonify
import spider

app = Flask(__name__)


@app.route('/news/list', methods=['GET'])
def getNews():
    try:
        type = request.args.get("type", "SDXW", type=str)
        page = request.args.get("page", 1, type=int)
        result = spider.NewsSpider(type, page).toJson()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify(
            {
                "current_page": 1,
                "max_page": 1,
                "type": "",
                "data": {
                    "title": "解析失败",
                    "link": "",
                    "date": ""
                }
            }
        )


@app.route("/news/type", methods=['GET'])
def getTypeList():
    typeList = []
    for key, value in spider.typeMap.items():
        typeList.append({
            "type": key,
            "name": value.name,
            "link": value.link,
        })
    result = {
        "data": typeList
    }
    return jsonify(result)


@app.route('/news/content', methods=['GET'])
def getNewsDetail():
    try:
        link = request.args.get("link", type=str)
        result = spider.ContentSpider(link).toJson()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify(spider.NewsContent("解析失败", "", "", [], 0))


if __name__ == '__main__':
    app.run()
