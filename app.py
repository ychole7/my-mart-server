# app.py (검색 & 선택 통합 버전)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

NAVER_CLIENT_ID = "본인의_ID"
NAVER_CLIENT_SECRET = "본인의_Secret"

# [기능 1] 검색어에 따른 10개 리스트 가져오기
@app.route('/search_list')
def search_list():
    keyword = request.args.get('item', '')
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"
    headers = {"X-Naver-Client-Id": JVXLTxKKG6ETmKg6Bo0V, "X-Naver-Client-Secret": 9JqlY6N21r}
    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        results = [{"title": i['title'].replace('<b>','').replace('</b>',''), "price": int(i['lprice']), "img": i['image']} for i in items]
        return jsonify(results)
    except: return jsonify([])

# [기능 2] 선택된 특정 상품명으로 4대 마트 정밀 수색
@app.route('/get_marts')
def get_marts():
    full_name = request.args.get('full_name', '')
    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    
    for mart in marts:
        # 선택된 상품명 뒤에 마트 이름을 붙여서 검색 (정밀도 상승)
        search_query = f"{full_name} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=5"
        headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            for item in items:
                mall = item['mallName']
                if mart in mall or (mart == "이마트" and "emart" in mall.lower()):
                    real_prices[mart] = {"price": int(item['lprice']), "title": item['title'].replace('<b>','').replace('</b>','')}
                    break
        except: continue
    return jsonify(real_prices)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
