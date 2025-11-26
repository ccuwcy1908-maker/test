import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse

# ==========================================
# 1. 核心設定
# ==========================================
st.set_page_config(page_title="2025 首爾行", page_icon="🇰🇷", layout="centered")

# ==========================================
# 2. iOS 風格極致 CSS (還原截圖)
# ==========================================
st.markdown("""
    <style>
    /* 1. 全局背景：純黑 */
    .stApp { background-color: #000000 !important; }
    
    /* 2. 字體顏色：全白 */
    h1, h2, h3, h4, p, span, div, label { 
        color: #FFFFFF !important; 
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif; 
    }
    
    /* 3. 卡片容器 (模仿截圖中的深灰區塊) */
    div.css-card {
        background-color: #1C1C1E;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #2C2C2E;
    }
    
    /* 4. 時間標籤 (右上角的藍色時間) */
    .time-badge {
        background-color: rgba(10, 132, 255, 0.15);
        color: #0A84FF !important;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        float: right;
    }
    
    /* 5. 標題與圖示 */
    .card-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* 6. 描述文字 */
    .card-desc {
        color: #8E8E93 !important; /* iOS 灰色 */
        font-size: 14px;
        margin-bottom: 20px;
        line-height: 1.4;
    }
    
    /* 7. 交通資訊 (左下角) */
    .transport-info {
        color: #8E8E93 !important;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 8. 按鈕樣式 (右下角藍色按鈕) */
    /* 由於 Streamlit 按鈕很難完全移動位置，我們透過 CSS 強制美化 */
    div.stButton > button, a[data-testid="stLinkButton"] {
        background-color: #0A84FF !important;
        color: white !important;
        border: none;
        border-radius: 20px; /* 更圓一點 */
        font-weight: 600;
        font-size: 14px;
        padding: 8px 16px;
        height: auto;
        min-height: 36px;
    }
    
    /* 9. Tab 分頁 (模擬底部導航的視覺感，雖然在上面) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #000000; 
        padding-bottom: 10px;
        border-bottom: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #8E8E93 !important; 
        border: none;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0A84FF !important; /* 選中變藍色 */
        font-weight: bold;
    }
    
    /* 隱藏 Plotly 工具列 */
    .modebar { display: none !important; }
    
    /* 隱藏 Streamlit 預設間距 */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 功能函式庫
# ==========================================

def get_naver_map_link(k_name, name):
    query = k_name if k_name else name
    encoded_query = urllib.parse.quote(query)
    # 使用 Naver Map 手機版連結
    return f"https://m.map.naver.com/search2/search.naver?query={encoded_query}"

@st.cache_data(ttl=3600)
def get_hourly_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-05"
        r = requests.get(url).json()
        hourly = r['hourly']
        df = pd.DataFrame({
            'time': pd.to_datetime(hourly['time']),
            'temp': hourly['temperature_2m']
        })
        return df
    except:
        return None

def plot_weather_chart(df):
    # 篩選 08:00 - 23:00
    day_df = df[(df['time'].dt.hour >= 8) & (df['time'].dt.hour <= 23)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=day_df['time'], y=day_df['temp'],
        mode='lines',
        line=dict(color='#0A84FF', width=3), # iOS Blue
        fill='tozeroy',
        fillcolor='rgba(10, 132, 255, 0.1)', # 藍色漸層
        hoverinfo='y'
    ))

    fig.update_layout(
        title=dict(text="🌤 12-05 氣溫走勢", font=dict(color="white", size=14)),
        paper_bgcolor='#1C1C1E', # 卡片背景色
        plot_bgcolor='#1C1C1E',
        margin=dict(l=20, r=20, t=40, b=20),
        height=180,
        showlegend=False,
        xaxis=dict(
            showgrid=False, 
            tickformat='%H:00', 
            tickfont=dict(color='#8E8E93', size=10),
            dtick=10800000.0 # 每3小時
        ),
        yaxis=dict(showgrid=False, visible=False, range=[day_df['temp'].min()-2, day_df['temp'].max()+5])
    )
    return fig

# ==========================================
# 4. 行程資料
# ==========================================
itinerary = {
    "12/5 (Day 1)": {
        "items": [
            {
                "time": "15:00", "title": "抵達/Check-in", "icon": "✈️",
                "desc": "機場快線 AREX 直達弘大，先去飯店放行李。", 
                "transport": "AREX 機場快線", "k_name": "홍대입구역", "loc": "Hongik Univ. Station"
            },
            {
                "time": "18:00", "title": "小豬存錢筒", "icon": "🍽",
                "desc": "弘大必吃石頭烤肉，石頭上烤的豬五花。", 
                "transport": "步行前往", "k_name": "돼지저금통", "loc": "Piggy Bank Stone Grill"
            },
            {
                "time": "20:00", "title": "弘大商圈", "icon": "🛍",
                "desc": "街頭表演、美妝、買衣服、拍貼機。", 
                "transport": "步行", "k_name": "홍대거리", "loc": "Hongdae Street"
            }
        ]
    },
    "12/6 (Day 2)": {
        "items": [
            {"time": "11:00", "title": "馬場洞韓牛", "icon": "🥩", "desc": "頂級 1++ 韓牛，推薦龍門家。", "transport": "馬場站", "k_name": "마장축산물시장", "loc": "Majang Meat Market"},
            {"time": "15:30", "title": "龍山 I’Park", "icon": "🛍", "desc": "超大購物中心，有龍貓展。", "transport": "龍山站", "k_name": "용산 아이파크몰", "loc": "I'Park Mall"},
            {"time": "18:30", "title": "一隻雞", "icon": "🍲", "desc": "蒜味濃郁雞湯。", "transport": "東大門", "k_name": "진옥화할매원조닭한마리", "loc": "Jin Ok-hwa Halmae"},
            {"time": "20:30", "title": "梨泰院", "icon": "🍸", "desc": "異國風情夜生活。", "transport": "梨泰院", "k_name": "이태원거리", "loc": "Itaewon Street"}
        ]
    },
    "12/7 (Day 3)": {
        "items": [
            {"time": "10:30", "title": "金豬食堂", "icon": "🐷", "desc": "米其林推薦 (需排隊)。", "transport": "藥水站", "k_name": "금돼지식당", "loc": "Gold Pig Dining"},
            {"time": "13:30", "title": "明洞商圈", "icon": "🛍", "desc": "Olive Young、明洞聖堂。", "transport": "明洞站", "k_name": "명동거리", "loc": "Myeongdong Street"},
            {"time": "18:00", "title": "無垢屋", "icon": "🍽", "desc": "清淡牛肉湯。", "transport": "市廳站", "k_name": "무구옥", "loc": "Muguok"}
        ]
    }
}

# ==========================================
# 5. App 主介面邏輯
# ==========================================

# 1. Header (模仿截圖的大標題)
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div style="margin-top: 10px;">
        <span style="font-size: 32px; font-weight: 800; color: white;">2025 首爾行</span>
        <span style="font-size: 24px;">🇰🇷</span>
    </div>
    """, unsafe_allow_html=True)

# 倒數計時
today = datetime.now()
trip_start = datetime(2025, 12, 5)
days_left = (trip_start - today).days
if days_left > 0:
    st.markdown(f"<p style='color:#FF453A !important; font-weight:600; font-size: 14px; margin-top: -10px;'>🚀 距離出發還有 {days_left} 天</p>", unsafe_allow_html=True)

st.write("") # Spacer

# 2. 氣溫圖表 (固定顯示 Day 1 或當天)
weather_df = get_hourly_weather()
if weather_df is not None:
    # 為了達到圓角卡片效果，我們把 Plotly 背景設為透明，然後外面包一層 div
    st.markdown('<div class="css-card" style="padding: 0px; overflow: hidden;">', unsafe_allow_html=True)
    fig = plot_weather_chart(weather_df)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Tab 導航
tab1, tab2, tab3, tab_money, tab_backup = st.tabs(["第一天", "第二天", "第三天", "分帳", "備案"])

# 4. 卡片渲染函數 (核心 UI)
def render_card(item):
    map_url = get_naver_map_link(item.get('k_name'), item['loc'])
    
    # HTML 結構模擬截圖
    st.markdown(f"""
    <div class="css-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div class="card-title">
                <span>{item['icon']}</span>
                <span>{item['title']}</span>
            </div>
            <div class="time-badge">{item['time']}</div>
        </div>
        <div class="card-desc">
            {item['desc']}
        </div>
        <div style="height: 1px; background-color: #333; margin-bottom: 15px;"></div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="transport-info">
                <span>🚇</span>
                <span>{item['transport']}</span>
            </div>
            <!-- 按鈕位置，Streamlit 的按鈕無法直接塞進 HTML，我們用 Columns 解決 -->
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 為了讓按鈕出現在卡片右下角，我們使用一點排版技巧
    # 注意：在 Streamlit 純 HTML 中很難放 Python 按鈕，
    # 這裡我們使用視覺上的 trick：在卡片下方緊接著放按鈕，透過 CSS 往上拉，或者把按鈕放在卡片結構外但視覺上像在裡面。
    # 
    # 最穩定的做法：
    # 上面的 HTML 負責顯示資訊，下方用 st.columns 放置按鈕 (如截圖中的導航)
    
    # 這裡我們用一個特殊的排版來模擬截圖中按鈕在卡片內的感覺
    # 因為 st.link_button 不能嵌在 markdown 裡，我們將卡片拆成兩部分，或把按鈕獨立出來
    
    # 修正方案：將按鈕獨立顯示在卡片下方，但透過 CSS 調整間距
    col_spacer, col_btn = st.columns([2, 1])
    with col_btn:
        st.link_button("✈️ 導航", map_url)
    
    # 用 CSS 把按鈕往上推，讓它看起來在卡片裡 (Optional, 視需求微調)
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) button {
        margin-top: -70px; /* 強制往上移 */
        position: relative;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. 渲染行程
with tab1:
    for item in itinerary["12/5 (Day 1)"]["items"]:
        render_card(item)

with tab2:
    for item in itinerary["12/6 (Day 2)"]["items"]:
        render_card(item)

with tab3:
    for item in itinerary["12/7 (Day 3)"]["items"]:
        render_card(item)

with tab_money:
    st.info("請前往 Line 群組記帳")
    st.link_button("🚀 開啟 Line 分帳", "https://line.me")

with tab_backup:
    st.markdown('<div class="css-card"><div class="card-title">☔️ Coex 星空圖書館</div><div class="card-desc">室內雨天備案。</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="css-card"><div class="card-title">🛍 樂天超市</div><div class="card-desc">首爾站買伴手禮。</div></div>', unsafe_allow_html=True)
