from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ 여기에 본인이 발급받은 키를 넣으세요!
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V"
NAVER_CLIENT_SECRET = "9JqlY6N21r"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword:
        return jsonify({"name": "No Item", "price": 0, "imgUrl": ""})

    # 네이버 정식 쇼핑 검색 API 주소
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=1"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            # lprice가 최저가입니다. <b> 태그는 제거합니다.
            return jsonify({
                "name": item['title'].replace('<b>', '').replace('</b>', ''),
                "price": int(item['lprice']),
                "imgUrl": item['image']
            })
        
        return jsonify({"name": keyword, "price": 0, "imgUrl": "", "msg": "검색 결과 없음"})
    except Exception as e:
        return jsonify({"name": keyword, "price": 0, "imgUrl": "", "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
