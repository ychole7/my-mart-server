from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 연칠님의 API 키 (따옴표 확인 필수!)
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

# [기능 1] 네이버 쇼핑에서 7개 상품 목록만 가져오기
@app.route('/search_list')
def search_list():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify([])
    # 7개만 요청
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=7"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        return jsonify([{
            "title": i['title'].replace('<b>','').replace('</b>',''),
            "price": int(i['lprice']),
            "img": i['image']
        } for i in items])
    except: return jsonify([])

# [기능 2] 선택한 특정 상품명으로 4대 마트 가격 정밀 수색
@app.route('/get_marts')
def get_marts():
    full_name = request.args.get('full_name', '')
    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    
    for mart in marts:
        search_query = f"{full_name} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=3"
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
