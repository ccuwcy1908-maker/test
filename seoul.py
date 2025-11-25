import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# ==========================================
# 1. 核心設定 & 成員名單
# ==========================================
st.set_page_config(page_title="首爾行 2024", page_icon="🇰🇷", layout="centered")

# 成員名單
MEMBERS = ["ChiYeh", "Olivia", "Yue", "May"]

# 初始化分帳資料庫
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ==========================================
# 2. CSS 樣式 (高對比配色：白底黑字)
# ==========================================
st.markdown("""
    <style>
    /* 強制背景白、文字黑 */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, div, span, li, .stMarkdown, label { color: #000000 !important; }
    
    /* 輸入框與選單文字顏色修正 */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stMultiSelect div {
        color: #000000 !important;
        background-color: #F0F2F6 !important; /* 淺灰底讓輸入框明顯一點 */
    }
    
    /* 按鈕樣式 */
    div.stButton > button {
        background-color: #007AFF !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    
    /* 數據指標卡 */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #000000 !important; }
    
    /* 表格樣式 */
    [data-testid="stDataFrame"] { border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 功能函式庫
# ==========================================

def get_apple_maps_link(lat, lon, name):
    return f"https://maps.apple.com/?q={name}&ll={lat},{lon}"

def get_weather():
    try:
        # 抓取 12/5 - 12/7 首爾天氣
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
# 4. 行程資料
# ==========================================
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

backup_plans = [
    {"name": "Coex 星空圖書館", "desc": "室內雨天備案"},
    {"name": "漢南洞逛街", "desc": "設計師品牌"},
    {"name": "樂天超市 (首爾站)", "desc": "伴手禮採買"}
]

# ==========================================
# 5. App 主介面
# ==========================================

st.title("🇰🇷 首爾行 2024")

# 天氣區塊
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
    st.caption("無法取得天氣資料")

st.markdown("---")

# 建立分頁：行程 + 分帳
tab1, tab2, tab3, tab_money, tab_backup = st.tabs(["D1", "D2", "D3", "💰 分帳", "備案"])

# --- 行程分頁函數 ---
def show_day(day):
    for item in itinerary[day]:
        with st.container():
            st.markdown(f"**{item['time']} {item['title']}**")
            st.markdown(f"📝 {item['desc']}")
            st.markdown(f"🚇 {item['transport']}")
            map_url = get_apple_maps_link(item['lat'], item['lon'], item['loc'])
            st.link_button("📍 Apple Maps", map_url)
            st.divider()

with tab1: show_day("12/5 (Day 1)")
with tab2: show_day("12/6 (Day 2)")
with tab3: show_day("12/7 (Day 3)")

# --- 💰 分帳功能分頁 ---
with tab_money:
    st.subheader("💸 旅費計算機")
    
    # 新增消費表單
    with st.expander("➕ 新增一筆消費", expanded=True):
        with st.form("expense_form"):
            col1, col2 = st.columns(2)
            item = col1.text_input("消費項目", placeholder="ex. 烤肉")
            amount = col2.number_input("金額 (KRW)", min_value=0, step=1000)
            
            payer = st.selectbox("誰先付錢？", MEMBERS)
            sharers = st.multiselect("誰要分擔？", MEMBERS, default=MEMBERS)
            
            submitted = st.form_submit_button("記帳")
            
            if submitted and amount > 0 and sharers:
                per_person = amount / len(sharers)
                st.session_state.expenses.append({
                    "項目": item,
                    "總金額": amount,
                    "付款人": payer,
                    "分擔人": ", ".join(sharers),
                    "每人應付": int(per_person)
                })
                st.success(f"已新增：{item}")

    # 顯示帳目
    if st.session_state.expenses:
        st.markdown("### 🧾 消費明細")
        df = pd.DataFrame(st.session_state.expenses)
        
        # 顯示簡易表格
        st.dataframe(
            df[["項目", "總金額", "付款人", "每人應付"]], 
            use_container_width=True,
            hide_index=True
        )
        
        # 統計資訊
        total_spent = df["總金額"].sum()
        st.metric("目前總開銷 (KRW)", f"₩{total_spent:,}")
        
        # 簡單計算誰先墊了多少
        st.markdown("#### 🏆 誰先墊了多少錢？")
        paid_stats = df.groupby("付款人")["總金額"].sum()
        st.bar_chart(paid_stats)

        # 清除按鈕
        if st.button("🗑 清除所有帳目"):
            st.session_state.expenses = []
            st.rerun()
    else:
        st.info("目前還沒有記帳喔！")

# --- 備案分頁 ---
with tab_backup:
    for plan in backup_plans:
        st.markdown(f"**{plan['name']}**")
        st.caption(plan['desc'])
        st.divider()

# 底部緊急資訊
with st.expander("🆘 緊急資訊"):
    st.write("報警: 112 | 急救: 119")
    st.write("外交部: +82-10-9080-2761")
