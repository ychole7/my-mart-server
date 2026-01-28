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
... (<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Mart v8.0 - Final Full</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body { background-color: #e9ecef; margin: 0; padding: 20px; display: flex; justify-content: center; font-family: 'Noto Sans KR', sans-serif; color: #333; }
        .app-body { background: #f8f9fa; width: 100%; max-width: 480px; border-radius: 35px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.15); overflow: hidden; min-height: 95vh; position: relative; border: 4px solid #fff; }
        .app-header { display: flex; justify-content: space-between; align-items: center; padding: 25px; background: linear-gradient(145deg, #1B5E20, #2E7D32); color: white; }
        
        /* 즐겨찾기 */
        .fav-section { padding: 0 20px; margin-top: 15px; }
        .fav-title { font-size: 13px; font-weight: 700; color: #2E7D32; margin-bottom: 8px; }
        .fav-container { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 5px; scrollbar-width: none; }
        .fav-item { flex-shrink: 0; background: white; padding: 8px 15px; border-radius: 20px; font-size: 12px; border: 1px solid #eee; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

        /* 마트 필터 */
        .mart-filter { display: flex; justify-content: center; gap: 6px; margin: 15px 20px; flex-wrap: wrap; }
        .filter-chip { padding: 6px 14px; border-radius: 18px; font-size: 11px; cursor: pointer; background: #eee; color: #888; border: none; transition: 0.2s; font-weight: 500; }
        .filter-chip.active { background: #2E7D32; color: white; font-weight: 700; }

        /* 검색창 */
        .search-box { background: white; padding: 8px; border-radius: 18px; margin: 10px 20px; display: flex; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eee; }
        .search-input { flex: 1; padding: 10px; border: none; outline: none; font-size: 15px; }
        .search-btn { padding: 0 20px; background: #2E7D32; color: white; border: none; border-radius: 14px; font-weight: 700; cursor: pointer; }
        
        #searchResultOverlay { display: none; position: absolute; top: 165px; left: 20px; right: 20px; background: white; border-radius: 18px; box-shadow: 0 15px 40px rgba(0,0,0,0.2); z-index: 9999; max-height: 450px; overflow-y: auto; border: 2px solid #2E7D32; }
        .result-item { display: flex; align-items: center; padding: 12px; border-bottom: 1px solid #f5f5f5; cursor: pointer; }
        .result-item img { width: 45px; height: 45px; border-radius: 8px; margin-right: 12px; }

        /* 상품 카드 & 수량 조절 */
        .product-card { background: white; border-radius: 20px; padding: 18px; margin: 0 20px 15px 20px; position: relative; box-shadow: 0 8px 20px rgba(0,0,0,0.04); border: 1px solid #f0f0f0; }
        .qty-control { display: flex; align-items: center; gap: 10px; margin-top: 10px; background: #f8f9fa; padding: 5px 12px; border-radius: 12px; width: fit-content; }
        .qty-btn { background: white; border: 1px solid #ddd; width: 24px; height: 24px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        
        .star-btn { position: absolute; top: 15px; right: 45px; background: none; border: none; color: #FFD600; cursor: pointer; font-size: 20px; }
        .del-btn { position: absolute; top: 15px; right: 15px; background: #f5f5f5; border: none; color: #999; width: 26px; height: 26px; border-radius: 50%; cursor: pointer; }

        /* 가격 그리드 */
        .price-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 15px; }
        .price-item { padding: 12px; border-radius: 14px; background: #f8f9fa; text-align: center; border: 1px solid #eee; cursor: pointer; }
        .price-item.low { border: 2px solid #2E7D32; background: #E8F5E9; font-weight: 700; }
        .price-item.avg-fill { opacity: 0.6; border-style: dashed; }
        .price-item.hide { display: none; }
        
        .mart-badge { display: inline-block; padding: 4px 10px; border-radius: 12px; color: white; font-size: 10px; font-weight: 700; margin-bottom: 6px; }
        .mart-emart { background: #FFB300; color: #333; } .mart-homeplus { background: #D32F2F; } .mart-lotte { background: #D81B60; } .mart-hanaro { background: #009688; }

        /* 차트 & 하단 바 */
        .chart-container { background: white; padding: 20px; border-radius: 20px; margin: 0 20px 20px 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); }
        .chart-bar-bg { background: #eee; height: 12px; border-radius: 6px; overflow: hidden; margin-top: 6px; }
        .chart-bar-fill { background: #4CAF50; height: 100%; transition: width 0.8s ease; }
        .chart-bar-fill.best { background: linear-gradient(90deg, #FFD600, #FFAB00); }
        .total-floating-bar { background: #212529; color: white; padding: 18px; border-radius: 20px; text-align: center; margin: 20px; font-weight: 700; cursor: pointer; }
    </style>
</head>
<body>
    <div class="app-body">
        <div class="app-header">
            <div class="header-title"><h2>Smart Mart v8.0</h2><span>All-in-One Edition</span></div>
            <button onclick="if(confirm('전체 삭제할까요?')){items=[];saveAndRender();}" style="background:none; border:none; color:white; font-size:20px; cursor:pointer;">🗑️</button>
        </div>

        <div class="fav-section" id="favSection" style="display:none;">
            <div class="fav-title">⭐ 즐겨찾기</div>
            <div class="fav-container" id="favContainer"></div>
        </div>

        <div class="mart-filter">
            <button class="filter-chip active" id="f-이마트" onclick="toggleMart('이마트')">이마트</button>
            <button class="filter-chip active" id="f-홈플러스" onclick="toggleMart('홈플러스')">홈플러스</button>
            <button class="filter-chip active" id="f-롯데마트" onclick="toggleMart('롯데마트')">롯데마트</button>
            <button class="filter-chip active" id="f-하나로" onclick="toggleMart('하나로')">하나로</button>
        </div>

        <div class="chart-container" id="chartSection" style="display:none;"><div id="barCharts"></div></div>

        <div class="search-box">
            <input type="text" class="search-input" id="pName" placeholder="상품명 입력 (예: 신라면)" onkeypress="if(event.keyCode==13) get7List()">
            <button class="search-btn" id="searchBtn" onclick="get7List()">검색</button>
        </div>

        <div id="searchResultOverlay"></div>
        <div id="list" style="padding-bottom: 90px;"></div>
        <div class="total-floating-bar" id="summary" onclick="copyToClipboard()">장바구니가 비어있습니다</div>
    </div>

    <script>
        const SERVER_URL = "https://my-mart-server.onrender.com"; 
        
        let items = JSON.parse(localStorage.getItem('smart_mart_v8_items')) || [];
        let favorites = JSON.parse(localStorage.getItem('smart_mart_v8_fav')) || [];
        let activeMarts = ["이마트", "홈플러스", "롯데마트", "하나로"];
        let lastResults = [];

        const martBadges = { "이마트": "mart-emart", "홈플러스": "mart-homeplus", "롯데마트": "mart-lotte", "하나로": "mart-hanaro" };

        function toggleMart(m) {
            if (activeMarts.includes(m)) {
                if (activeMarts.length > 1) activeMarts = activeMarts.filter(x => x !== m);
                else alert("최소 한 마트는 켜두어야 합니다.");
            } else { activeMarts.push(m); }
            updateFilterUI();
            render();
        }

        function updateFilterUI() {
            document.querySelectorAll('.filter-chip').forEach(el => {
                const mName = el.id.split('-')[1];
                el.className = activeMarts.includes(mName) ? 'filter-chip active' : 'filter-chip';
            });
        }

        function toggleFav(idx) {
            const item = items[idx];
            const fIdx = favorites.findIndex(f => f.name === item.name);
            if (fIdx > -1) favorites.splice(fIdx, 1);
            else favorites.push({ name: item.name, img: item.imgUrl });
            localStorage.setItem('smart_mart_v8_fav', JSON.stringify(favorites));
            updateFavUI();
            render();
        }

        function updateFavUI() {
            const container = document.getElementById('favContainer');
            if (favorites.length === 0) { document.getElementById('favSection').style.display = 'none'; return; }
            document.getElementById('favSection').style.display = 'block';
            container.innerHTML = favorites.map(f => `<div class="fav-item" onclick="document.getElementById('pName').value='${f.name}';get7List();">${f.name}</div>`).join('');
        }

        async function get7List() {
            const name = document.getElementById('pName').value.trim();
            if(!name) return;
            const overlay = document.getElementById('searchResultOverlay');
            overlay.innerHTML = "<p style='text-align:center; padding:20px;'>🔍 목록 검색 중...</p>";
            overlay.style.display = "block";

            try {
                const res = await fetch(`${SERVER_URL.replace(/\/$/, "")}/search_list?item=${encodeURIComponent(name)}`);
                lastResults = await res.json();
                overlay.innerHTML = lastResults.map((item, i) => `
                    <div class="result-item" onclick="selectProduct(${i})">
                        <img src="${item.img}" onerror="this.src='https://via.placeholder.com/45'">
                        <div style="flex:1">
                            <div style="font-size:14px; font-weight:bold;">${item.title}</div>
                            <div style="font-size:12px; color:#E91E63;">${item.price.toLocaleString()}원~</div>
                        </div>
                    </div>`).join('');
            } catch(e) { overlay.style.display = "none"; }
        }

        async function selectProduct(idx) {
            const sel = lastResults[idx];
            document.getElementById('searchResultOverlay').style.display = "none";
            document.getElementById('pName').value = "";
            const tempId = Date.now();
            items.unshift({ id: tempId, name: sel.title, imgUrl: sel.img, qty: 1, loading: true, prices: {"이마트":{price:0}, "홈플러스":{price:0}, "롯데마트":{price:0}, "하나로":{price:0}} });
            render();
            try {
                const res = await fetch(`${SERVER_URL.replace(/\/$/, "")}/get_marts?full_name=${encodeURIComponent(sel.title)}`);
                const data = await res.json();
                const i = items.findIndex(x => x.id === tempId);
                if(i > -1) { items[i].prices = data; items[i].loading = false; saveAndRender(); }
            } catch(e) { console.error("가격 수집 오류"); }
        }

        function updateQty(idx, delta) {
            items[idx].qty = Math.max(1, (items[idx].qty || 1) + delta);
            saveAndRender();
        }

        function manualInput(idx, mart) {
            const cur = items[idx].prices[mart].price || 0;
            const price = prompt(`${mart} 가격을 입력하세요`, cur);
            if (price !== null && !isNaN(price)) {
                items[idx].prices[mart].price = parseInt(price);
                saveAndRender();
            }
        }

        function render() {
            const listDiv = document.getElementById('list');
            listDiv.innerHTML = '';
            let ts = {"이마트":0, "홈플러스":0, "롯데마트":0, "하나로":0};
            if(items.length === 0) { document.getElementById('chartSection').style.display = "none"; document.getElementById('summary').innerText = "장바구니가 비어있습니다."; return; }

            items.forEach((item, i) => {
                const ps = Object.values(item.prices).map(v => v.price).filter(p => p > 0);
                const avg = ps.length > 0 ? Math.round(ps.reduce((a,b)=>a+b)/ps.length) : 0;
                const min = ps.length > 0 ? Math.min(...ps) : 0;
                const isF = favorites.some(f => f.name === item.name);

                activeMarts.forEach(m => { ts[m] += (item.prices[m].price > 0 ? item.prices[m].price : avg) * item.qty; });

                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <button class="star-btn" onclick="toggleFav(${i})">${isF ? '★' : '☆'}</button>
                    <button class="del-btn" onclick="items.splice(${i},1);saveAndRender();">✕</button>
                    <div style="display:flex; align-items:center;">
                        <img src="${item.imgUrl}" style="width:40px; height:40px; border-radius:8px; margin-right:12px; border:1px solid #eee;">
                        <div style="font-weight:bold; font-size:14px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:200px;">${item.loading ? "⏳ 수색 중..." : item.name}</div>
                    </div>
                    <div class="qty-control">
                        <button class="qty-btn" onclick="updateQty(${i}, -1)">-</button>
                        <span style="font-size:13px; font-weight:bold;">${item.qty}개</span>
                        <button class="qty-btn" onclick="updateQty(${i}, 1)">+</button>
                    </div>
                    <div class="price-grid">
                        ${Object.entries(item.prices).map(([m, info]) => {
                            const show = activeMarts.includes(m);
                            const p = info.price > 0 ? info.price : avg;
                            return `<div class="price-item ${!show ? 'hide' : ''} ${info.price === min && info.price > 0 ? 'low' : ''} ${info.price === 0 ? 'avg-fill' : ''}" onclick="manualInput(${i}, '${m}')">
                                <span class="mart-badge ${martBadges[m]}">${m}</span>
                                <div style="font-size:14px; font-weight:700;">${p === 0 ? '-' : p.toLocaleString()+'원'}</div>
                                ${info.price === 0 && avg > 0 ? '<div style="font-size:9px; opacity:0.6;">(평균가)</div>' : ''}
                            </div>`;
                        }).join('')}
                    </div>`;
                listDiv.appendChild(card);
            });
            updateChart(ts);
        }

        function updateChart(ts) {
            const chartSection = document.getElementById('chartSection');
            chartSection.style.display = "block";
            const max = Math.max(...activeMarts.map(m => ts[m]));
            const best = activeMarts.reduce((a, b) => ts[a] > 0 && ts[a] < (ts[b] || Infinity) ? a : b);
            document.getElementById('barCharts').innerHTML = activeMarts.map(m => `
                <div style="margin-bottom:10px;"><div style="font-size:11px; display:flex; justify-content:space-between; margin-bottom:4px;"><span>${m}</span><b>${ts[m].toLocaleString()}원</b></div>
                <div class="chart-bar-bg"><div class="chart-bar-fill ${m === best ? 'best' : ''}" style="width:${(ts[m]/max)*100}%"></div></div></div>`).join('');
            document.getElementById('summary').innerHTML = `🏆 추천 마트: <span style="color:#FFD600; font-size:1.1em;">${best}</span> (공유하기)`;
        }

        function copyToClipboard() {
            if (items.length === 0) return;
            let text = `[스마트 마트 장바구니]\n`;
            items.forEach(item => { text += `- ${item.name} (${item.qty}개)\n`; });
            navigator.clipboard.writeText(text).then(() => alert("리스트가 복사되었습니다!"));
        }

        function saveAndRender() { localStorage.setItem('smart_mart_v8_items', JSON.stringify(items)); render(); }
        window.onclick = function(e) {
            const overlay = document.getElementById('searchResultOverlay');
            if (e.target !== document.getElementById('pName') && e.target !== document.getElementById('searchBtn') && !overlay.contains(e.target)) overlay.style.display = 'none';
        }
        updateFavUI();
        render();
    </script>
</body>
</html>) ...
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

