import requests
from config import AUTH_KEY
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/getWords/<word>")
def get_words(word) :
    url = f"https://stdict.korean.go.kr/api/search.do?key={AUTH_KEY}&req_type=json&q={word}"
    response = requests.get(url)

    if (response.status_code == 200) :
        data = response.json()
        itemMap = data["channel"]["item"]

    wordList = []
    for item in itemMap :
        sup_no = item["sup_no"]
        definition = item["sense"]["definition"]
        pos = item["pos"]

        wordList.append(
            {
                "sup_no" : sup_no,
                "definition" : definition,
                "pos" : pos
            }
        )
    
    return jsonify(
        {
            "searchWord" : word,
            "wordList" : wordList
        }
    )



### Run Flask
if __name__ == "__main__" :
    app.run(port = 8000, debug = True)