import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests

# ==========================================
# 1. 核心設定 & iOS 優化
# ==========================================
st.set_page_config(page_title="首爾行 2024", page_icon="🇰🇷", layout="centered")

# CSS: 隱藏多餘選單，優化手機觸控體驗，仿 iOS 卡片風格
st.markdown("""
    <style>
    /* 全局字體與背景 */
    .stApp {background-color: #F2F2F7;} /* iOS 淺灰色背景 */
    
    /* 隱藏 Streamlit 預設漢堡選單與 Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 卡片樣式 */
    .css-1r6slb0, .stMarkdown, .stMetric {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    /* 按鈕樣式 (仿 iOS 藍色按鈕) */
    div.stButton > button {
        background-color: #007AFF;
        color: white;
        border-radius: 12px;
        border: none;
        height: 50px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
    
    /* Tab 樣式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 功能函式庫
# ==========================================

# 取得 Apple Maps 連結 (強制 iOS 開啟地圖 App)
def get_apple_maps_link(lat, lon, name):
    # iOS URL Scheme: maps://?q=Name&ll=Lat,Lon
    return f"https://maps.apple.com/?q={name}&ll={lat},{lon}"

# 取得天氣 (使用 Open-Meteo 免費 API)
def get_weather():
    try:
        # 首爾座標
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-07"
        r = requests.get(url).json()
        return r['daily']
    except:
        return None

# 天氣代碼轉換為 Emoji
def weather_icon(code):
    if code <= 3: return "☀️ 晴朗"
    if code <= 48: return "☁️ 多雲/陰"
    if code <= 67: return "🌧️ 下雨"
    if code <= 77: return "❄️ 下雪"
    return "🌤️"

# ==========================================
# 3. 資料庫 (行程與備案)
# ==========================================

# 備案清單
backup_plans = [
    {"name": "Coex 星空圖書館", "desc": "室內雨天備案，拍照好看", "loc": "Coex Mall"},
    {"name": "漢南洞逛街", "desc": "如果梨泰院太吵，來這裡逛設計師品牌", "loc": "Hannam-dong"},
    {"name": "樂天超市 (首爾站)", "desc": "買伴手禮最後衝刺", "loc": "Lotte Mart Seoul Station"},
    {"name": "廣藏市場", "desc": "如果不想吃餐廳，來這吃綠豆煎餅", "loc": "Gwangjang Market"}
]

# 行程詳細資料 (包含座標用於導航)
itinerary = {
    "12/5 (Day 1)": [
        {"time": "15:00", "title": "✈️ 抵達/Check-in", "desc": "機場快線 -> 弘大飯店", "transport": "AREX 機場快線 (約50分)", "lat": 37.5575, "lon": 126.9245, "loc": "Hongik Univ. Station"},
        {"time": "18:00", "title": "🍽 小豬存錢筒", "desc": "必吃石頭烤肉，需排隊", "transport": "步行前往", "lat": 37.5559, "lon": 126.9230, "loc": "Piggy Bank Stone Grill"},
        {"time": "20:00", "title": "🛍 弘大商圈", "desc": "逛街、拍貼機、買襪子", "transport": "步行", "lat": 37.5563, "lon": 126.9225, "loc": "Hongdae Street"}
    ],
    "12/6 (Day 2)": [
        {"time": "11:00", "title": "🥩 馬場洞韓牛", "desc": "先買肉再上樓，推薦龍門家", "transport": "地鐵5號線 馬場站 2號出口", "lat": 37.5670, "lon": 127.0420, "loc": "Majang Meat Market"},
        {"time": "14:00", "title": "📷 證件照拍攝", "desc": "記得帶妝，預約信要存好", "transport": "地鐵移動", "lat": 37.5560, "lon": 126.9240, "loc": "Photostudio"},
        {"time": "15:30", "title": "🛍 龍山 I’Park", "desc": "逛相機、Switch、龍貓展", "transport": "地鐵1號線 龍山站", "lat": 37.5298, "lon": 126.9647, "loc": "I'Park Mall"},
        {"time": "18:30", "title": "🍲 一隻雞 (晚餐)", "desc": "陳玉華或孔陵，湯頭清甜", "transport": "地鐵4號線 東大門站", "lat": 37.5709, "lon": 127.0062, "loc": "Jin Ok-hwa Halmae"},
        {"time": "20:30", "title": "🍸 梨泰院酒吧", "desc": "Fountain / Thursday Party", "transport": "地鐵6號線 梨泰院站", "lat": 37.5340, "lon": 126.9940, "loc": "Itaewon Street"}
    ],
    "12/7 (Day 3)": [
        {"time": "10:30", "title": "🐷 金豬食堂", "desc": "米其林推薦，開店前先去寫名單", "transport": "地鐵3號線 藥水站", "lat": 37.5590, "lon": 127.0100, "loc": "Gold Pig Dining"},
        {"time": "13:30", "title": "🛍 明洞商圈", "desc": "Olive Young 旗艦店補貨", "transport": "地鐵4號線 明洞站", "lat": 37.5630, "lon": 126.9840, "loc": "Myeongdong Street"},
        {"time": "18:00", "title": "🍽 無垢屋", "desc": "最後的晚餐：清淡牛肉湯", "transport": "地鐵1/2號線 市廳站", "lat": 37.5650, "lon": 126.9790, "loc": "Muguok"}
    ]
}

# ==========================================
# 4. App 介面開始
# ==========================================

# --- 首頁總覽區 ---
st.title("🇰🇷 SEOUL TRIP")
today = datetime.now()
trip_start = datetime(2025, 12, 5)
days_left = (trip_start - today).days

# 資訊摘要卡片
col1, col2 = st.columns([2, 3])
with col1:
    if days_left > 0:
        st.metric("倒數計時", f"{days_left} 天", "準備出發")
    elif days_left == 0:
        st.metric("狀態", "就是今天!", "Have Fun!")
    else:
        st.metric("狀態", "旅程進行中", "Day " + str(abs(days_left)+1))

with col2:
    st.caption(f"📅 目前日期：{today.strftime('%m/%d %H:%M')}")
    st.info("💡 點擊行程可直接開啟 Apple Maps")

# --- 天氣資訊區 ---
st.subheader("🌦 當地天氣")
weather_data = get_weather()

if weather_data:
    # 建立橫向捲動的天氣卡
    w_cols = st.columns(3)
    dates = ["12/5", "12/6", "12/7"]
    
    for i in range(3):
        with w_cols[i]:
            code = weather_data['weather_code'][i]
            min_t = weather_data['temperature_2m_min'][i]
            max_t = weather_data['temperature_2m_max'][i]
            
            st.write(f"**{dates[i]}**")
            st.write(f"{weather_icon(code)}")
            st.caption(f"{min_t}° ~ {max_t}°")
            
            # 穿衣建議
            if min_t < 0:
                st.warning("⚠️ 極凍：發熱衣+羽絨")
            elif min_t < 10:
                st.info("🧥 冷：大衣+圍巾")
else:
    st.error("無法取得天氣資訊，請檢查網路")

st.divider()

# --- 每日行程表 (Tab 切換) ---
st.subheader("📅 行程導覽")
tab1, tab2, tab3, tab4 = st.tabs(["Day 1", "Day 2", "Day 3", "備選方案"])

def render_itinerary(day_key):
    for item in itinerary[day_key]:
        with st.container():
            # 使用兩欄佈局：左邊時間，右邊內容
            c1, c2 = st.columns([1, 4])
            with c1:
                st.write(f"**{item['time']}**")
            with c2:
                # 標題與說明
                st.markdown(f"**{item['title']}**")
                st.caption(f"{item['desc']}")
                
                # 交通與導航按鈕區
                with st.expander("🚇 交通 & 導航", expanded=False):
                    st.write(f"🚊 **{item['transport']}**")
                    # Apple Maps 深層連結按鈕
                    map_url = get_apple_maps_link(item['lat'], item['lon'], item['loc'])
                    st.link_button("🗺️ 開啟 Apple Maps 導航", map_url)
            st.divider()

with tab1:
    render_itinerary("12/5 (Day 1)")
with tab2:
    render_itinerary("12/6 (Day 2)")
with tab3:
    render_itinerary("12/7 (Day 3)")
with tab4:
    st.write("### ☔️ 雨天/備用行程")
    for plan in backup_plans:
        st.write(f"**📍 {plan['name']}**")
        st.caption(plan['desc'])
        st.markdown(f"[🔍 在 Google 搜尋 {plan['name']}](https://www.google.com/search?q=首爾+{plan['name']})")
        st.divider()

# --- 底部工具 ---
with st.expander("🛠 設定與匯率"):
    st.write("此區域可連接記帳功能或緊急聯絡資訊")
    st.write("📞 韓國報警：112 | 急救：119")
    st.write("🇰🇷 外交部緊急聯絡：+82-10-9080-2761")
