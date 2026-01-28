# app.py (정밀 저격수 버전)
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V"
NAVER_CLIENT_SECRET = "9JqlY6N21r"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify({})

    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: 0 for m in marts}
    img_url = ""

    # 각 마트별로 정밀 검색 실시
    for mart in marts:
        # 검색어 예: "신라면 5입 이마트"
        search_query = f"{keyword} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=10"
        headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}

        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            
            for item in items:
                mall = item['mallName']
                # 해당 마트 이름이 들어간 결과물 중 가장 첫 번째(최저가)를 선택
                if (mart in mall or (mart == "이마트" and "emart" in mall.lower())):
                    real_prices[mart] = int(item['lprice'])
                    if not img_url: img_url = item['image']
                    break # 찾았으면 해당 마트 검색 종료
        except:
            continue

    return jsonify({
        "name": keyword,
        "prices": real_prices,
        "imgUrl": img_url
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
