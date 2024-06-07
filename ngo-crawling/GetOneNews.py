import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/getOneNews", methods=["GET"])
def get_one_news() :
    media = request.args.get("media")
    article = request.args.get("article")

    response = requests.get(f"https://n.news.naver.com/mnews/article/{media}/{article}")

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
    
        return jsonify(
            {
                "title" : title,
                "summary" : summary,
                "contents" : contents,
                "media" : media,
                "editor" : editor,
                "thumbnail" : thumbnail,
                "media_id" : media,
                "article_id" : article
            }
        )
    
    return None


if __name__ == "__main__" :
    port = int(os.environ.get("PORT", 8005))
    app.run(host="0.0.0.0", port=port)