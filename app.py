from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import re

app = Flask(__name__)
CORS(app)

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword:
        return jsonify({"name": "No Item", "price": 0, "imgUrl": ""})

    url = f"https://msearch.shopping.naver.com/search/all?query={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://m.naver.com/"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        
        # [핵심] 네이버 쇼핑이 숨겨둔 진짜 데이터 뭉치(__NEXT_DATA__)를 통째로 낚아챕니다.
        match = re.search(r'id="__NEXT_DATA__" type="application/json">({.*?})</script>', res.text)
        
        if match:
            all_data = json.loads(match.group(1))
            # 데이터 뭉치 안에서 가격과 이미지 경로를 차례로 타고 들어갑니다.
            products = all_data['props']['pageProps']['initialState']['products']['list']
            if products:
                top_product = products[0]['item']
                return jsonify({
                    "name": top_product['productName'],
                    "price": int(top_product['lowPrice']),
                    "imgUrl": top_product['imageUrl']
                })
        
        return jsonify({"name": keyword, "price": 0, "imgUrl": "", "msg": "데이터 구조 찾기 실패"})
    except Exception as e:
        return jsonify({"name": keyword, "price": 0, "imgUrl": "", "error": str(e)})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
