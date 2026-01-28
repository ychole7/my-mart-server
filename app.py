from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 네이버 API 키
NAVER_CLIENT_ID = "JVXLTxKKG6ETmKg6Bo0V" 
NAVER_CLIENT_SECRET = "9JqlY6N21r"

# [핵심] 여기에 연칠님의 HTML 코드 전체를 넣습니다.
HTML_CODE = """
<!DOCTYPE html>
<html lang="ko">
... (여기에 연칠님이 쓰시던 v8.0 HTML 코드 전체를 복사해서 넣으세요) ...
</html>
"""

# 1. 대문 주소로 들어오면 위 HTML 화면을 보여줍니다.
@app.route('/')
def index():
    # HTML 내부의 SERVER_URL을 현재 서버 주소로 자동 변경 (중요!)
    # 이 부분은 서버 주소를 직접 안 고쳐도 되게 만들어줍니다.
    return render_template_string(HTML_CODE)

# 2. 7개 목록 가져오기
@app.route('/search_list')
def search_list():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify([])
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=7"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        return jsonify([{"title": i['title'].replace('<b>','').replace('</b>',''), "price": int(i['lprice']), "img": i['image']} for i in items])
    except: return jsonify([])

# 3. 마트 가격 가져오기
@app.route('/get_marts')
def get_marts():
    full_name = request.args.get('full_name', '')
    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    for mart in marts:
        url = f"https://openapi.naver.com/v1/search/shop.json?query={full_name} {mart}&display=3"
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
