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
# 2. iOS 風格極致 CSS
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
    
    /* 3. 卡片容器 */
    div.css-card {
        background-color: #1C1C1E;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #2C2C2E;
    }
    
    /* 4. 時間標籤 */
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
        color: #8E8E93 !important; 
        font-size: 14px;
        margin-bottom: 20px;
        line-height: 1.4;
    }
    
    /* 7. 交通資訊 */
    .transport-info {
        color: #8E8E93 !important;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 8. 按鈕樣式 */
    div.stButton > button, a[data-testid="stLinkButton"] {
        background-color: #0A84FF !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        padding: 8px 16px;
        height: auto;
        min-height: 36px;
    }
    
    /* 9. Tab 分頁 */
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
        color: #0A84FF !important;
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
    return f"https://m.map.naver.com/search2/search.naver?query={encoded_query}"

@st.cache_data(ttl=3600)
def get_hourly_weather():
    try:
        # 這裡改成一次抓 3 天 (12/05 - 12/07)
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-07"
        r = requests.get(url).json()
        hourly = r['hourly']
        df = pd.DataFrame({
            'time': pd.to_datetime(hourly['time']),
            'temp': hourly['temperature_2m']
        })
        return df
    except:
        return None

def plot_weather_chart(df, target_date_str):
    # 根據傳入的日期字串 (YYYY-MM-DD) 篩選資料
    target_date = pd.to_datetime(target_date_str).date()
    day_df = df[df['time'].dt.date == target_date].copy()
    
    # 篩選 08:00 - 23:00
    day_df = day_df[(day_df['time'].dt.hour >= 8) & (day_df['time'].dt.hour <= 23)]
    
    if day_df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=day_df['time'], 
        y=day_df['temp'],
        mode='lines+text', 
        text=[f"{t:.0f}°" for t in day_df['temp']], 
        textposition="top center", 
        textfont=dict(color='white', size=12, family="Arial"),
        line=dict(color='#0A84FF', width=3), 
        fill='tozeroy',
        fillcolor='rgba(10, 132, 255, 0.1)', 
        hoverinfo='y'
    ))

    # 計算 Y 軸範圍
    min_temp = day_df['temp'].min()
    max_temp = day_df['temp'].max()

    # 格式化標題日期 MM-DD
    title_date = target_date.strftime("%m-%d")

    fig.update_layout(
        title=dict(text=f"🌤 {title_date} 氣溫走勢", font=dict(color="white", size=14)),
        paper_bgcolor='#1C1C1E', 
        plot_bgcolor='#1C1C1E',
        margin=dict(l=20, r=20, t=50, b=20),
        height=200,
        showlegend=False,
        xaxis=dict(
            showgrid=False, 
            tickformat='%H', 
            tickfont=dict(color='#8E8E93', size=10),
            dtick=10800000.0 
        ),
        yaxis=dict(
            showgrid=False, 
            visible=False, 
            range=[min_temp - 2, max_temp + 5]
        )
    )
    return fig

# ==========================================
# 4. 行程資料 (加入日期欄位)
# ==========================================
itinerary = {
    "12/5 (Day 1)": {
        "date": "2025-12-05",
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
        "date": "2025-12-06",
        "items": [
            {"time": "11:00", "title": "馬場洞韓牛", "icon": "🥩", "desc": "頂級 1++ 韓牛，推薦龍門家。", "transport": "馬場站", "k_name": "마장축산물시장", "loc": "Majang Meat Market"},
            {"time": "15:30", "title": "龍山 I’Park", "icon": "🛍", "desc": "超大購物中心，有龍貓展。", "transport": "龍山站", "k_name": "용산 아이파크몰", "loc": "I'Park Mall"},
            {"time": "18:30", "title": "一隻雞", "icon": "🍲", "desc": "蒜味濃郁雞湯。", "transport": "東大門", "k_name": "진옥화할매원조닭한마리", "loc": "Jin Ok-hwa Halmae"},
            {"time": "20:30", "title": "梨泰院", "icon": "🍸", "desc": "異國風情夜生活。", "transport": "梨泰院", "k_name": "이태원거리", "loc": "Itaewon Street"}
        ]
    },
    "12/7 (Day 3)": {
        "date": "2025-12-07",
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

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div style="margin-top: 10px;">
        <span style="font-size: 32px; font-weight: 800; color: white;">2025 首爾行</span>
        <span style="font-size: 24px;">🇰🇷</span>
    </div>
    """, unsafe_allow_html=True)

today = datetime.now()
trip_start = datetime(2025, 12, 5)
days_left = (trip_start - today).days
if days_left > 0:
    st.markdown(f"<p style='color:#FF453A !important; font-weight:600; font-size: 14px; margin-top: -10px;'>🚀 距離出發還有 {days_left} 天</p>", unsafe_allow_html=True)

st.write("") 

# 取得 3 天的天氣資料
weather_df = get_hourly_weather()

# Tab 導航
tab1, tab2, tab3, tab_money, tab_backup = st.tabs(["第一天", "第二天", "第三天", "分帳", "備案"])

# 卡片渲染函數
def render_card(item):
    map_url = get_naver_map_link(item.get('k_name'), item['loc'])
    
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
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_spacer, col_btn = st.columns([2, 1])
    with col_btn:
        st.link_button("✈️ 導航", map_url)
    
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) button {
        margin-top: -70px;
        position: relative;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

# 共用頁面渲染函數
def render_page(day_key):
    # 1. 先顯示當天的氣溫圖
    day_data = itinerary[day_key]
    if weather_df is not None:
        fig = plot_weather_chart(weather_df, day_data['date'])
        if fig:
            st.markdown('<div class="css-card" style="padding: 0px; overflow: hidden;">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    # 2. 再顯示當天的行程卡片
    for item in day_data['items']:
        render_card(item)

# 渲染各分頁
with tab1: render_page("12/5 (Day 1)")
with tab2: render_page("12/6 (Day 2)")
with tab3: render_page("12/7 (Day 3)")

with tab_money:
    st.info("請前往 Line 群組記帳")
    st.link_button("🚀 開啟 Line 分帳", "https://liff.line.me/1655320992-Y8GowEpw/g/pEHGMZAzu5UAyZXX4F268P")

with tab_backup:
    st.markdown('<div class="css-card"><div class="card-title">☔️ Coex 星空圖書館</div><div class="card-desc">室內雨天備案。</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="css-card"><div class="card-title">🛍 樂天超市</div><div class="card-desc">首爾站買伴手禮。</div></div>', unsafe_allow_html=True)
