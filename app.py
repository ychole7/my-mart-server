from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# 1. CORS 설정: 외부(우리 앱)에서 이 서버에 접속하는 것을 허용합니다.
CORS(app)

# 2. 네이버 API 키 설정 (반드시 따옴표로 감싸주세요!)
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

# [루트 1] 검색어 입력 시 네이버에서 상품 10개 리스트 가져오기
@app.route('/search_list')
def search_list():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify([])

    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        # 앱에서 쓰기 좋게 상품명, 가격, 이미지만 골라냅니다.
        results = [{
            "title": i['title'].replace('<b>','').replace('</b>',''), 
            "price": int(i['lprice']), 
            "img": i['image']
        } for i in items]
        return jsonify(results)
    except Exception as e:
        print(f"Error in search_list: {e}")
        return jsonify([])

# [루트 2] 선택한 상품으로 4대 마트 가격 정밀 수색하기
@app.route('/get_marts')
def get_marts():
    full_name = request.args.get('full_name', '')
    if not full_name: return jsonify({})

    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    for mart in marts:
        # 검색어 예: "신라면 5개입 이마트"
        search_query = f"{full_name} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=5"
        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            for item in items:
                mall = item['mallName']
                # 마트 이름이 포함된 결과 중 최상단 가격 선택
                if mart in mall or (mart == "이마트" and "emart" in mall.lower()):
                    real_prices[mart] = {
                        "price": int(item['lprice']),
                        "title": item['title'].replace('<b>','').replace('</b>','')
                    }
                    break
        except:
            continue
            
    return jsonify(real_prices)

if __name__ == "__main__":
    # Render 환경에서 포트를 자동으로 잡아주도록 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

