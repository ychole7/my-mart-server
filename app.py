from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ [중요] 여기에 본인의 API 키를 꼭 따옴표 안에 넣어주세요!
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify({})

    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    img_url = ""

    # 각 마트별 정밀 검색 (Sniper Search)
    for mart in marts:
        search_query = f"{keyword} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=5"
        headers = {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
        }

        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            
            for item in items:
                mall = item['mallName']
                # 마트 이름이 포함된 결과 중 최저가 선택
                if (mart in mall or (mart == "이마트" and "emart" in mall.lower())):
                    real_prices[mart] = {
                        "price": int(item['lprice']),
                        "title": item['title'].replace('<b>','').replace('</b>','')
                    }
                    if not img_url: img_url = item['image']
                    break
        except:
            continue

    return jsonify({
        "name": keyword,
        "prices": real_prices,
        "imgUrl": img_url
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
