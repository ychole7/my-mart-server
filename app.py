# app.py (실시간 실측 엔진)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V"
NAVER_CLIENT_SECRET = "9JqlY6N21r"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify([])

    # 검색 결과 100개를 가져와서 마트별 가격을 솎아냅니다.
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=100"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}

    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        
        # 실제 마트별 가격 저장소 (0은 정보 없음)
        real_prices = {"이마트": 0, "홈플러스": 0, "롯데마트": 0, "하나로": 0}
        img_url = items[0]['image'] if items else ""

        for item in items:
            mall = item['mallName']
            price = int(item['lprice'])
            
            # 판매처 이름에 마트명이 포함된 경우만 가격 추출
            if ("emart" in mall.lower() or "이마트" in mall) and real_prices["이마트"] == 0:
                real_prices["이마트"] = price
            elif "홈플러스" in mall and real_prices["홈플러스"] == 0:
                real_prices["홈플러스"] = price
            elif "롯데마트" in mall and real_prices["롯데마트"] == 0:
                real_prices["롯데마트"] = price
            elif "하나로" in mall and real_prices["하나로"] == 0:
                real_prices["하나로"] = price

        # 사용자가 선택할 수 있게 검색 결과 리스트도 함께 반환 (간략화)
        return jsonify({
            "name": keyword,
            "prices": real_prices,
            "imgUrl": img_url,
            "raw_list": [{"name": i['title'].replace('<b>','').replace('</b>',''), "price": int(i['lprice']), "img": i['image']} for i in items[:10]]
        })
    except:
        return jsonify({})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
