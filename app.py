from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ 본인의 API 키를 따옴표 안에 꼭 넣어주세요!
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify({})

    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    img_url = ""

    # 각 마트별 정밀 검색 (v4.2에서 성공했던 그 로직)
    for mart in marts:
        search_query = f"{keyword} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=5"
        headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            for item in items:
                mall = item['mallName']
                if mart in mall or (mart == "이마트" and "emart" in mall.lower()):
                    real_prices[mart] = {
                        "price": int(item['lprice']),
                        "title": item['title'].replace('<b>','').replace('</b>','')
                    }
                    if not img_url: img_url = item['image']
                    break
        except: continue

    return jsonify({"name": keyword, "prices": real_prices, "imgUrl": img_url})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
