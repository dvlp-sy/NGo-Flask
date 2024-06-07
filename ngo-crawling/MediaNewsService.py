import os
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/getMediaNews", methods=["GET"])
def get_media_news() :
    q_media = request.args.get("oid")
    q_date = request.args.get("date")

    response = requests.get(f"https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid={q_media}&listType=paper&date={q_date}")
    if (response.status_code == 200) :
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        newsList = []
        for i in range(5, 26, 2) :
            image = soup.select_one(f"#main_content > div.list_body.newsflash_body > ul:nth-child({i}) > li:nth-child(1) > dl > dt.photo > a > img")
            if image != None :
                image = image["src"]
            else : 
                image = None

            mainUrl = soup.select_one(f"#main_content > div.list_body.newsflash_body > ul:nth-child({i}) > li:nth-child(1) > dl > dt:nth-child(2) > a")
            if mainUrl != None :
                mainUrl = mainUrl["href"]
            else : 
                mainUrl = None

            title = soup.select_one(f"#main_content > div.list_body.newsflash_body > ul:nth-child({i}) > li:nth-child(1) > dl > dt:nth-child(2) > a")
            if title != None :
                title = title.text
            else : 
                title = ""

            summary = soup.select_one(f"#main_content > div.list_body.newsflash_body > ul:nth-child({i}) > li:nth-child(1) > dl > dd > span.lede.\\38 8")
            if summary != None :
                summary = summary.text
            else : 
                summary = ""
            
            urlList = []
            for j in range(2, 6) :
                url = soup.select_one(f"#main_content > div.list_body.newsflash_body > ul:nth-child({i}) > li:nth-child({j}) > dl > dt > a")
                if url != None :
                    url = url["href"]
                    urlList.append(url)

            if ((mainUrl != None) and (title != None)) :
                newsList.append(
                    {
                        "mainUrl" : mainUrl,
                        "image" : image,
                        "title" : title,
                        "summary" : summary,
                        "urlList" : urlList
                    }
                )

        return jsonify(
            {
                "newsList" : newsList
            }
        )


### Run Flask
if __name__ == "__main__" :
    port = int(os.environ.get("PORT", 8004))
    app.run(host="0.0.0.0", port=port)