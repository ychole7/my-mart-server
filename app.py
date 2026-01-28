from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ 연칠님의 네이버 API 키
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

# [기능 1] 7개 목록 가져오기 (이 경로가 있어야 앱이 작동합니다)
@app.route('/search_list')
def search_list():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify([])
    
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=7"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    
    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        # 데이터가 잘 나오는지 서버 로그에 찍어봅니다.
        print(f"검색어 {keyword} 결과: {len(items)}개 찾음")
        return jsonify([{
            "title": i['title'].replace('<b>','').replace('</b>',''),
            "price": int(i['lprice']),
            "img": i['image']
        } for i in items])
    except Exception as e:
        print(f"서버 에러: {e}")
        return jsonify([])

# [기능 2] 선택한 상품으로 4대 마트 가격 정밀 수색
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
