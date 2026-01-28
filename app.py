# app.py (실시간 실측 버전)
@app.route('/get_price')
def get_price():
    keyword = request.args.get('item', '')
    if not keyword: return jsonify({})

    # 검색 결과 100개를 가져와서 마트별 가격을 솎아냅니다.
    url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=100"
    headers = {
        "X-Naver-Client-Id": JVXLTxKKG6ETmKg6Bo0V,
        "X-Naver-Client-Secret": 9JqlY6N21r
    }

    try:
        res = requests.get(url, headers=headers)
        items = res.json().get('items', [])
        
        # 실제 마트별 가격 저장소 (0은 못 찾았음을 의미)
        real_prices = {"이마트": 0, "홈플러스": 0, "롯데마트": 0, "하나로": 0}
        img_url = ""

        for item in items:
            mall_name = item['mallName']
            price = int(item['lprice'])
            if not img_url: img_url = item['image']

            # 마트 이름이 포함된 판매처의 가격만 매칭
            if "emart" in mall_name.lower() or "이마트" in mall_name:
                if real_prices["이마트"] == 0: real_prices["이마트"] = price
            elif "홈플러스" in mall_name:
                if real_prices["홈플러스"] == 0: real_prices["홈플러스"] = price
            elif "롯데마트" in mall_name:
                if real_prices["롯데마트"] == 0: real_prices["롯데마트"] = price
            elif "하나로" in mall_name:
                if real_prices["하나로"] == 0: real_prices["하나로"] = price

        return jsonify({
            "name": keyword,
            "prices": real_prices,
            "imgUrl": img_url
        })
    except:
        return jsonify({})
