from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import os  # Render의 포트 설정을 위해 필요합니다.

app = Flask(__name__)
CORS(app)

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword:
        return jsonify({"name": "No Item", "price": 0, "imgUrl": ""})

    search_query = f"{keyword} 최저가"
    url = f"https://msearch.shopping.naver.com/search/all?query={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        # 가격 추출 (더 정교한 정규표현식)
        price_match = re.search(r'(\d{1,3}(?:,\d{3})*)원', res.text)
        price_val = int(price_match.group(1).replace(',', '')) if price_match else 0
        
        # 이미지 추출
        img_match = re.search(r'https://shopping-phinf.pstatic.net/[^"]+?\.jpg', res.text)
        img_url = img_match.group(0) if img_match else ""

        return jsonify({"name": keyword, "price": price_val, "imgUrl": img_url})
    except:
        return jsonify({"name": keyword, "price": 0, "imgUrl": ""})

# Render에서 서버를 띄우기 위한 필수 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)