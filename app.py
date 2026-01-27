from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword:
        return jsonify({"name": "No Item", "price": 0, "imgUrl": ""})

    # 검색 정확도를 위해 '최저가' 키워드 추가
    url = f"https://msearch.shopping.naver.com/search/all?query={keyword}"
    
    # 네이버를 속이기 위한 더 정교한 '사람 코스프레' 헤더
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://m.naver.com/"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        
        # [방식 1] 가장 흔한 가격 패턴 찾기 (10,000원)
        price_match = re.search(r'(\d{1,3}(?:,\d{3})*)원', res.text)
        
        # [방식 2] 혹시 없으면 다른 패턴 시도 (숫자만 있는 경우)
        if not price_match:
            price_match = re.search(r'price":"(\d+)"', res.text)

        if price_match:
            # 쉼표 제거 후 숫자로 변환
            price_str = price_match.group(1).replace(',', '')
            price_val = int(price_str)
        else:
            price_val = 0
        
        # 이미지 주소 찾기
        img_match = re.search(r'https://shopping-phinf.pstatic.net/[^"]+?\.jpg', res.text)
        img_url = img_match.group(0) if img_match else ""

        return jsonify({
            "name": keyword, 
            "price": price_val, 
            "imgUrl": img_url
        })
    except Exception as e:
        # 에러가 나면 어떤 에러인지 슬쩍 보여줍니다 (디버깅용)
        return jsonify({"name": keyword, "price": 0, "imgUrl": "", "error": str(e)})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
