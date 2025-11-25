import streamlit as st
from datetime import datetime
import requests

# ==========================================
# 1. 核心設定 (修正配色問題)
# ==========================================
st.set_page_config(page_title="首爾行 2024", page_icon="🇰🇷", layout="centered")

# CSS: 強制使用高對比配色 (白底黑字)
st.markdown("""
    <style>
    /* 1. 強制應用程式背景為白色 */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* 2. 強制所有主要文字為深黑色 */
    h1, h2, h3, p, div, span, li, .stMarkdown {
        color: #000000 !important;
    }
    
    /* 3. 卡片區塊樣式：加上淺灰邊框，背景微白，確保文字清楚 */
    div[data-testid="stExpander"], div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
        border-radius: 8px;
    }

    /* 4. Tab 分頁標籤文字修正 */
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
    }
    
    /* 5. 按鈕維持高對比藍底白字 */
    div.stButton > button {
        background-color: #007AFF !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
        border-radius: 8px;
    }
    
    /* 6. 修正 Metric 指標卡 (倒數天數那邊) */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 功能函式庫
# ==========================================

# Apple Maps 連結
def get_apple_maps_link(lat, lon, name):
    return f"https://maps.apple.com/?q={name}&ll={lat},{lon}"

# 取得天氣 (API)
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-07"
        r = requests.get(url).json()
        return r['daily']
    except:
        return None

def weather_icon(code):
    if code <= 3: return "☀️"
    if code <= 48: return "☁️"
    if code <= 67: return "🌧️"
    if code <= 77: return "❄️"
    return "🌤️"

# ==========================================
# 3. 行程資料
# ==========================================
backup_plans = [
    {"name": "Coex 星空圖書館", "desc": "室內雨天備案", "loc": "Coex Mall"},
    {"name": "漢南洞逛街", "desc": "設計師品牌集中地", "loc": "Hannam-dong"},
    {"name": "樂天超市 (首爾站)", "desc": "買零食伴手禮", "loc": "Lotte Mart Seoul Station"}
]

itinerary = {
    "12/5 (Day 1)": [
        {"time": "15:00", "title": "✈️ 抵達/Check-in", "desc": "機場快線 -> 弘大飯店", "transport": "AREX 機場快線", "lat": 37.5575, "lon": 126.9245, "loc": "Hongik Univ. Station"},
        {"time": "18:00", "title": "🍽 小豬存錢筒", "desc": "石頭烤肉 (弘大)", "transport": "步行前往", "lat": 37.5559, "lon": 126.9230, "loc": "Piggy Bank Stone Grill"},
        {"time": "20:00", "title": "🛍 弘大商圈", "desc": "逛街、拍貼機", "transport": "步行", "lat": 37.5563, "lon": 126.9225, "loc": "Hongdae Street"}
    ],
    "12/6 (Day 2)": [
        {"time": "11:00", "title": "🥩 馬場洞韓牛", "desc": "先買肉再上樓 (龍門家)", "transport": "5號線 馬場站 2號出口", "lat": 37.5670, "lon": 127.0420, "loc": "Majang Meat Market"},
        {"time": "14:00", "title": "📷 證件照拍攝", "desc": "記得帶妝、準時到", "transport": "地鐵移動", "lat": 37.5560, "lon": 126.9240, "loc": "Photostudio"},
        {"time": "15:30", "title": "🛍 龍山 I’Park", "desc": "電子商場、龍貓展", "transport": "1號線 龍山站", "lat": 37.5298, "lon": 126.9647, "loc": "I'Park Mall"},
        {"time": "18:30", "title": "🍲 一隻雞 (晚餐)", "desc": "陳玉華或孔陵", "transport": "4號線 東大門站", "lat": 37.5709, "lon": 127.0062, "loc": "Jin Ok-hwa Halmae"},
        {"time": "20:30", "title": "🍸 梨泰院酒吧", "desc": "Fountain / Thursday Party", "transport": "6號線 梨泰院站", "lat": 37.5340, "lon": 126.9940, "loc": "Itaewon Street"}
    ],
    "12/7 (Day 3)": [
        {"time": "10:30", "title": "🐷 金豬食堂", "desc": "米其林推薦，早點去寫名單", "transport": "3號線 藥水站", "lat": 37.5590, "lon": 127.0100, "loc": "Gold Pig Dining"},
        {"time": "13:30", "title": "🛍 明洞商圈", "desc": "Olive Young、明洞聖堂", "transport": "4號線 明洞站", "lat": 37.5630, "lon": 126.9840, "loc": "Myeongdong Street"},
        {"time": "18:00", "title": "🍽 無垢屋", "desc": "清淡牛肉湯", "transport": "1號線 市廳站", "lat": 37.5650, "lon": 126.9790, "loc": "Muguok"}
    ]
}

# ==========================================
# 4. App 介面
# ==========================================

st.title("🇰🇷 首爾旅遊助手")

# --- 資訊摘要 ---
today = datetime.now()
trip_start = datetime(2025, 12, 5)
days_left = (trip_start - today).days

st.info(f"📅 今天是：{today.strftime('%m/%d')}｜距離出發還有 **{days_left}** 天")

# --- 天氣 ---
st.subheader("🌦 預報")
weather_data = get_weather()
if weather_data:
    cols = st.columns(3)
    dates = ["12/5", "12/6", "12/7"]
    for i in range(3):
        with cols[i]:
            code = weather_data['weather_code'][i]
            min_t = weather_data['temperature_2m_min'][i]
            max_t = weather_data['temperature_2m_max'][i]
            st.metric(label=dates[i], value=f"{weather_icon(code)}", delta=f"{min_t}°-{max_t}°")
else:
    st.warning("暫時無法取得天氣")

st.markdown("---")

# --- 行程 ---
st.subheader("📍 每日行程")
st.caption("點擊按鈕可直接開啟 Apple Maps")

tab1, tab2, tab3, tab4 = st.tabs(["Day 1", "Day 2", "Day 3", "備案"])

def show_day(day):
    for item in itinerary[day]:
        with st.container():
            # 簡單乾淨的排版
            st.markdown(f"### {item['time']} {item['title']}")
            st.markdown(f"📝 {item['desc']}")
            st.markdown(f"🚇 **{item['transport']}**")
            
            # 導航按鈕
            map_url = get_apple_maps_link(item['lat'], item['lon'], item['loc'])
            st.link_button("🗺️ 開啟導航 (Apple Maps)", map_url)
            st.markdown("---")

with tab1: show_day("12/5 (Day 1)")
with tab2: show_day("12/6 (Day 2)")
with tab3: show_day("12/7 (Day 3)")

with tab4:
    for plan in backup_plans:
        st.markdown(f"**{plan['name']}**")
        st.write(plan['desc'])
        st.markdown("---")

# --- 緊急資訊 ---
with st.expander("🆘 緊急聯絡"):
    st.write("**報警**：112")
    st.write("**急救**：119")
    st.write("**外交部緊急聯絡**：+82-10-9080-2761")
