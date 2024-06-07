import os
import requests
import re
from requests_toolbelt import MultipartEncoder
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

def limit(text) :
    ## 특수문자 제한
    regExp = re.compile(r'[^ㄱ-힣a-zA-Z0-9\.\?\,\!\s]', re.UNICODE) 
    regExpEmoji = re.compile(r'[\U0001F000-\U0001F9FF]', re.UNICODE)
    text = regExp.sub("", text)
    text = regExpEmoji.sub("", text)
    return text

def format(text, max_len) :
    text = limit(text)
    if (len(text) > max_len) :
        return text[:max_len]
    else :
        return text


def fetchLevel(title, content) :

    # POST (KreadNo 값 불러오기)
    post_url = "https://www.kread.ai/api/v1/kread/insert"
    title = format(title, 100)
    content = format(content, 1000)
    form_data = {
        "userTp": "ET",
        "docuTp": "R",
        "dataTp": "TEXT",
        "title": title,
        "contents": content
    }
    header = {
        "Content-Type" : "multipart/form-data; boundary=----WebKitFormBoundaryBB7CU3zBBGxE9Fix"
    }

    multipart = MultipartEncoder(fields=form_data, boundary="----WebKitFormBoundaryBB7CU3zBBGxE9Fix", encoding="UTF-8")

    if (title != None and content != None) :
        response = requests.post(post_url, data=multipart, headers=header)
        post_data = response.json()
        if response.status_code == 200 :
            kreadNo = post_data["data"]["kreadNo"]



    # GET (level 요청하기)
    get_url = f"https://www.kread.ai/api/v1/kread/detail?kreadNo={kreadNo}"
    response = requests.get(get_url)
    get_data = response.json()
    count = 1

    while (response.status_code != 200 or get_data["data"]["status"] != 2) and count <= 30 :
        response = requests.get(get_url)
        get_data = response.json()
        count += 1
        print(count)

    if kreadNo != None :
        return get_data["data"]["score"]
    else :
        return 2000


@app.route("/getLevel", methods=["GET"])
def get_level() :
    # 정치 = 100 | 경제 = 101 | 사회 = 102 | 생활/문화 = 103 | 과학 = 105
    query = request.args.get("category")

    if query :
        result = []

        # getNews (by Category)
        url = f"http://news-server-01:8001/getNews?category={query}"
        response = requests.get(url)
        if response.status_code == 200 :
            data = response.json()

            # result 추출 및 level에 따른 내림차순 정렬
            newsList = data["news"]
            for news in newsList :
                title = news["title"]
                content = news["contents"]
                level = fetchLevel(title, content)
                result.append(
                    {
                        "title" : news["title"],
                        "contents" : news["contents"],
                        "media" : news["media"],
                        "editor" : news["editor"],
                        "thumbnail" : news["thumbnail"],
                        "summary" : news["summary"],
                        "level" : level,
                        "media_code" : news["media_code"],
                        "article_code" : news["article_code"]
                    }
                )
        
        return jsonify(
            {
                "news" : sorted(result, key=lambda x: x["level"])
            }
        )
    


### Run Flask
if __name__ == "__main__" :
    port = int(os.environ.get("PORT", 8002))
    app.run(host="0.0.0.0", port=port)