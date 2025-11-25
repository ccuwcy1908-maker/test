import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# 1. 核心設定 & 成員名單
# ==========================================
st.set_page_config(page_title="首爾行 2025", page_icon="🇰🇷", layout="centered")

MEMBERS = ["ChiYeh", "Olivia", "Yue", "May"]
EXCHANGE_RATE = 43.5 

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# ==========================================
# 2. 極致美化 CSS (深色質感風格)
# ==========================================
st.markdown("""
    <style>
    /* 全局設定 */
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, h4, p, span, div, label { color: #FFFFFF !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* 卡片風格 (微透明深灰) */
    div[data-testid="stExpander"], div.stContainer {
        background-color: #1C1C1E;
        border-radius: 16px;
        border: 1px solid #333333;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* 圖片圓角與陰影 */
    img { border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    
    /* Tab 分頁美化 */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #121212; 
        border-radius: 20px; 
        padding: 5px; 
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 15px;
        color: #888888 !important;
        flex: 1; /* 平均分配寬度 */
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #2C2C2E;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* 輸入框美化 */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stMultiSelect div {
        background-color: #2C2C2E !important;
        color: white !important;
        border-radius: 10px;
        border: none;
    }
    
    /* 按鈕美化 (漸層藍) */
    div.stButton > button {
        background: linear-gradient(135deg, #0A84FF 0%, #0056b3 100%) !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 12px rgba(10, 132, 255, 0.3);
    }
    
    /* 隱藏 Plotly 工具列 */
    .modebar { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 功能函式庫 (含 Hourly 天氣)
# ==========================================

def get_apple_maps_link(lat, lon, name):
    return f"https://maps.apple.com/?q={name}&ll={lat},{lon}"

@st.cache_data(ttl=3600) # 快取 1 小時，避免重複 call API
def get_hourly_weather():
    try:
        # 抓取 2025/12/5 - 12/7 的 Hourly 資料
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-07"
        r = requests.get(url).json()
        
        # 整理資料
        hourly = r['hourly']
        df = pd.DataFrame({
            'time': pd.to_datetime(hourly['time']),
            'temp': hourly['temperature_2m'],
            'rain': hourly['precipitation_probability']
        })
        return df
    except:
        return None

def plot_weather_chart(df, target_date_str):
    """ 繪製美觀的 Plotly 氣溫圖 """
    # 篩選當天資料 (08:00 - 23:00 活動時間)
    target_date = pd.to_datetime(target_date_str).date()
    day_df = df[df['time'].dt.date == target_date].copy()
    day_df = day_df[(day_df['time'].dt.hour >= 8) & (day_df['time'].dt.hour <= 23)]
    
    if day_df.empty:
        return None

    # 建立圖表
    fig = go.Figure()

    # 1. 氣溫線 (漸層填充)
    fig.add_trace(go.Scatter(
        x=day_df['time'], y=day_df['temp'],
        mode='lines+text',
        name='氣溫',
        line=dict(color='#0A84FF', width=3),
        fill='tozeroy', # 填充顏色
        fillcolor='rgba(10, 132, 255, 0.1)',
        text=[f"{t:.0f}°" for t in day_df['temp']], # 顯示數值
        textposition="top center",
        textfont=dict(color='white', size=12)
    ))

    # 設定圖表外觀
    fig.update_layout(
        title=dict(text=f"🌡️ {target_date_str[5:]} 氣溫趨勢", font=dict(color="white", size=14)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        height=200,
        showlegend=False,
        xaxis=dict(
            showgrid=False, 
            tickformat='%H:00', 
            tickfont=dict(color='#888'),
            tickmode='linear',
            dtick=10800000.0 # 每3小時一格
        ),
        yaxis=dict(showgrid=False, visible=False, range=[day_df['temp'].min()-2, day_df['temp'].max()+3])
    )
    return fig

# ==========================================
# 4. 行程資料
# ==========================================
itinerary = {
    "12/5 (Day 1)": {
        "date": "2025-12-05",
        "items": [
            {"time": "15:00", "title": "✈️ 抵達/Check-in", "desc": "機場快線 -> 弘大飯店", "transport": "AREX 機場快線", "lat": 37.5575, "lon": 126.9245, "loc": "Hongik Univ. Station", "img": "https://images.unsplash.com/photo-1538485399081-7191377e8241?q=80&w=600&auto=format&fit=crop"},
            {"time": "18:00", "title": "🍽 小豬存錢筒", "desc": "石頭烤肉 (弘大)｜必點豬五花", "transport": "步行前往", "lat": 37.5559, "lon": 126.9230, "loc": "Piggy Bank Stone Grill", "img": "https://images.unsplash.com/photo-1627993079624-94c0347a8a0f?q=80&w=600&auto=format&fit=crop"},
            {"time": "20:00", "title": "🛍 弘大商圈", "desc": "逛街、拍貼機、街頭表演", "transport": "步行", "lat": 37.5563, "lon": 126.9225, "loc": "Hongdae Street", "img": "https://images.unsplash.com/photo-1580910543632-132d75b8db5e?q=80&w=600&auto=format&fit=crop"}
        ]
    },
    "12/6 (Day 2)": {
        "date": "2025-12-06",
        "items": [
            {"time": "11:00", "title": "🥩 馬場洞韓牛", "desc": "1++ 韓牛｜先買肉再上樓 (龍門家)", "transport": "5號線 馬場站 2號出口", "lat": 37.5670, "lon": 127.0420, "loc": "Majang Meat Market", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Korean_beef-Hanau.jpg/640px-Korean_beef-Hanau.jpg"},
            {"time": "14:00", "title": "📷 證件照拍攝", "desc": "記得帶妝、準時到攝影棚", "transport": "地鐵移動", "lat": 37.5560, "lon": 126.9240, "loc": "Photostudio", "img": "https://images.unsplash.com/photo-1520390138845-fd2d229dd552?q=80&w=600&auto=format&fit=crop"},
            {"time": "15:30", "title": "🛍 龍山 I’Park", "desc": "電子商場、龍貓展、百貨", "transport": "1號線 龍山站", "lat": 37.5298, "lon": 126.9647, "loc": "I'Park Mall", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/I%27Park_Mall_Yongsan_Station.jpg/640px-I%27Park_Mall_Yongsan_Station.jpg"},
            {"time": "18:30", "title": "🍲 一隻雞 (晚餐)", "desc": "陳玉華或孔陵｜蒜味雞湯", "transport": "4號線 東大門站", "lat": 37.5709, "lon": 127.0062, "loc": "Jin Ok-hwa Halmae", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Dak-hanmari.jpg/640px-Dak-hanmari.jpg"},
            {"time": "20:30", "title": "🍸 梨泰院酒吧", "desc": "Fountain / Thursday Party", "transport": "6號線 梨泰院站", "lat": 37.5340, "lon": 126.9940, "loc": "Itaewon Street", "img": "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?q=80&w=600&auto=format&fit=crop"}
        ]
    },
    "12/7 (Day 3)": {
        "date": "2025-12-07",
        "items": [
            {"time": "10:30", "title": "🐷 金豬食堂", "desc": "米其林推薦｜開店前先去寫名單", "transport": "3號線 藥水站", "lat": 37.5590, "lon": 127.0100, "loc": "Gold Pig Dining", "img": "https://images.unsplash.com/photo-1596910547037-846b1980329f?q=80&w=600&auto=format&fit=crop"},
            {"time": "13:30", "title": "🛍 明洞商圈", "desc": "Olive Young 旗艦店、明洞聖堂", "transport": "4號線 明洞站", "lat": 37.5630, "lon": 126.9840, "loc": "Myeongdong Street", "img": "https://images.unsplash.com/photo-1538485399081-7191377e8241?q=80&w=600&auto=format&fit=crop"},
            {"time": "18:00", "title": "🍽 無垢屋", "desc": "清淡牛肉湯、韓式拌麵", "transport": "1號線 市廳站", "lat": 37.5650, "lon": 126.9790, "loc": "Muguok", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Gomguk.jpg/640px-Gomguk.jpg"}
        ]
    }
}

backup_plans = [
    {"name": "Coex 星空圖書館", "desc": "室內雨天備案", "img": "https://images.unsplash.com/photo-1625723044792-44de168af407?q=80&w=600&auto=format&fit=crop"},
    {"name": "漢南洞逛街", "desc": "設計師品牌", "img": "https://images.unsplash.com/photo-1549144511-30858b340096?q=80&w=600&auto=format&fit=crop"},
    {"name": "樂天超市 (首爾站)", "desc": "伴手禮採買", "img": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?q=80&w=600&auto=format&fit=crop"}
]

# ==========================================
# 5. App 主介面邏輯
# ==========================================

# Header
st.title("🇰🇷 2025 首爾行")
today = datetime.now()
trip_start = datetime(2025, 12, 5)
days_left = (trip_start - today).days

if days_left > 0:
    st.markdown(f"<p style='color:#0A84FF !important; font-weight:bold;'>🚀 距離出發還有 {days_left} 天</p>", unsafe_allow_html=True)

# 抓取天氣資料
weather_df = get_hourly_weather()

st.markdown("---")

# 建立分頁
tab1, tab2, tab3, tab_money, tab_backup = st.tabs(["Day 1", "Day 2", "Day 3", "💰 分帳", "備案"])

# --- 通用渲染函數 ---
def render_day_tab(day_key):
    day_data = itinerary[day_key]
    date_str = day_data['date']
    
    # 1. 顯示當天 Hourly 天氣圖表
    if weather_df is not None:
        fig = plot_weather_chart(weather_df, date_str)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.caption("尚無詳細氣象資料")
    
    # 2. 顯示行程卡片
    for item in day_data['items']:
        with st.container():
            # 圖片區
            if "img" in item:
                st.image(item["img"], use_container_width=True)
            
            # 標題與時間
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{item['title']}**")
            col2.markdown(f"*{item['time']}*")
            
            # 內容
            st.caption(item['desc'])
            
            # 底部資訊欄 (交通+導航)
            b1, b2 = st.columns([3, 2])
            b1.markdown(f"🚇 {item['transport']}")
            map_url = get_apple_maps_link(item['lat'], item['lon'], item['loc'])
            b2.link_button("📍 導航", map_url, use_container_width=True)

with tab1: render_day_tab("12/5 (Day 1)")
with tab2: render_day_tab("12/6 (Day 2)")
with tab3: render_day_tab("12/7 (Day 3)")

# --- 💰 分帳功能 ---
with tab_money:
    st.subheader("💸 旅費計算機")
    
    with st.expander("➕ 新增消費", expanded=True):
        with st.form("expense_form"):
            currency_type = st.radio("輸入幣別", ["韓元 (KRW)", "台幣 (TWD)"], horizontal=True)
            
            c1, c2 = st.columns(2)
            item = c1.text_input("項目", placeholder="ex. 烤肉")
            amount_input = c2.number_input("金額", min_value=0, step=100)
            
            payer = st.selectbox("付款人", MEMBERS)
            sharers = st.multiselect("分擔人", MEMBERS, default=MEMBERS)
            
            if st.form_submit_button("新增款項"):
                if amount_input > 0 and sharers:
                    if "台幣" in currency_type:
                        real_amount_krw = int(amount_input * EXCHANGE_RATE)
                        note = f"(NT${amount_input})"
                    else:
                        real_amount_krw = int(amount_input)
                        note = ""

                    per_person = real_amount_krw / len(sharers)
                    st.session_state.expenses.append({
                        "項目": item + f" {note}",
                        "金額(KRW)": real_amount_krw,
                        "付款人": payer,
                        "分擔人": ", ".join(sharers),
                        "每人(KRW)": int(per_person)
                    })
                    st.success("已新增")

    if st.session_state.expenses:
        st.markdown("### 🧾 消費明細")
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df[["項目", "金額(KRW)", "付款人", "每人(KRW)"]], use_container_width=True, hide_index=True)
        
        total = df["金額(KRW)"].sum()
        st.info(f"💰 總開銷：₩{total:,} (約 NT$ {int(total/EXCHANGE_RATE):,})")
        
        # 顯示統計圖
        chart_data = df.groupby("付款人")["金額(KRW)"].sum().reset_index()
        fig_bar = px.bar(chart_data, x='付款人', y='金額(KRW)', text_auto=True, color='付款人')
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_bar, use_container_width=True)

        if st.button("🗑 清除帳目"):
            st.session_state.expenses = []
            st.rerun()
    else:
        st.caption("尚未有消費紀錄")

# --- 備案 ---
with tab_backup:
    for plan in backup_plans:
        st.image(plan["img"], use_container_width=True)
        st.markdown(f"**📍 {plan['name']}**")
        st.caption(plan['desc'])
        st.divider()

# Footer
st.caption("2025 Seoul Trip App | Designed for iOS")
