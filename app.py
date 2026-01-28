from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ⚠️ 본인의 API 키를 그대로 유지하세요!
NAVER_CLIENT_ID = "발급받은_ID"
NAVER_CLIENT_SECRET = "발급받은_Secret"

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword:
        return jsonify([])

    # display=10: 검색 결과 10개를 가져옵니다.
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        results = []
        if 'items' in data:
            for item in data['items']:
                results.append({
                    "name": item['title'].replace('<b>', '').replace('</b>', ''),
                    "price": int(item['lprice']),
                    "imgUrl": item['image']
                })
        return jsonify(results) # 10개의 리스트를 보냅니다.
    except:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
