# app.py (정보 투명성 강화 버전)
@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify({})

    marts = ["이마트", "홈플러스", "롯데마트", "하나로"]
    real_prices = {m: {"price": 0, "title": "정보없음"} for m in marts}
    img_url = ""

    for mart in marts:
        search_query = f"{keyword} {mart}"
        url = f"https://openapi.naver.com/v1/search/shop.json?query={search_query}&display=5"
        headers = {"X-Naver-Client-Id": JVXLTxKKG6ETmKg6Bo0V, "X-Naver-Client-Secret": 9JqlY6N21r}

        try:
            res = requests.get(url, headers=headers)
            items = res.json().get('items', [])
            for item in items:
                mall = item['mallName']
                if (mart in mall or (mart == "이마트" and "emart" in mall.lower())):
                    # 가격과 실제 상품명을 함께 저장
                    real_prices[mart] = {
                        "price": int(item['lprice']),
                        "title": item['title'].replace('<b>','').replace('</b>','')
                    }
                    if not img_url: img_url = item['image']
                    break
        except: continue

    return jsonify({"name": keyword, "prices": real_prices, "imgUrl": img_url})
