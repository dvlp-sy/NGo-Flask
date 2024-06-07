import os
import requests
import re
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = Flask(__name__)

def parse_url(url) :
    pattern = r'/article/(\d+)/(\d+)'
    match_url = re.search(pattern, url)

    if match_url :
        media_code = match_url.group(1)
        article_code = match_url.group(2)
        return media_code, article_code
    else :
        return None, None
    
@app.route("/getNews", methods=["GET"])
def get_news() :
    # 정치 = 100 | 경제 = 101 | 사회 = 102 | 생활/문화 = 103 | 과학 = 105
    query = request.args.get("category")
    
    if query :
        data = requests.get(f"https://news.naver.com/section/{query}")

        urlList = []
        for i in range(1, 11) :
            html = data.text
            soup = BeautifulSoup(html, "html.parser")
            ul_tag = soup.find("ul", id=lambda x: x and x.startswith('_SECTION_HEADLINE_LIST_'))
            key = ul_tag["id"].split('_')[-1]

            a_href = soup.select_one(f"#_SECTION_HEADLINE_LIST_{key} > li:nth-child({i}) > div > div > div.sa_text > a")
            if a_href != None :
                url = a_href.get("href")
                urlList.append(url)
            else :
                url = None

        newsList = []
        for url in urlList :
            response = requests.get(url)
            if response.status_code == 200 :
                html = response.text
                soup = BeautifulSoup(html, "html.parser")

                media = soup.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top._LAZY_LOADING_WRAP > a > img.media_end_head_top_logo_img.light_type._LAZY_LOADING._LAZY_LOADING_INIT_HIDE")
                if media != None :
                    media = media.get("alt")
                else :
                    media = ""
                
                editor = soup.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_journalist > a > em")
                if editor != None : 
                    editor = editor.text
                else :
                    editor = ""

                title = soup.select_one("#title_area > span")
                if title != None : 
                    title = title.text
                else :
                    title = ""

                summary = soup.find("strong", class_="media_end_summary")
                if summary != None :
                    summary = summary.get_text().replace('<br>', '')
                else :
                    summary = ""

                contents = soup.find("article", id="dic_area")
                if contents != None :
                    contents = contents.get_text().replace('\n', '')
                else :
                    contents = ""

                thumbnail = soup.find("img", id="img1")
                if thumbnail != None :
                    thumbnail = thumbnail["data-src"]
                else :
                    thumbnail = ""

                media_code, article_code = parse_url(url)
                print(media_code, article_code)

                newsList.append(
                    {
                        "title" : title,
                        "summary" : summary,
                        "contents" : contents,
                        "media" : media,
                        "editor" : editor,
                        "thumbnail" : thumbnail,
                        "media_code" : media_code,
                        "article_code" : article_code
                    }
                )
            
        return jsonify(
            {
                "news" : newsList
            }
        )
    

### Run Flask
if __name__ == "__main__" :
    port = int(os.environ.get("PORT", 8001))
    app.run(host="0.0.0.0", port=port)