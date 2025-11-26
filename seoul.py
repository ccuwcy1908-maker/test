import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse # 用來處理網址編碼

# ==========================================
# 1. 核心設定
# ==========================================
st.set_page_config(page_title="首爾行 2025", page_icon="🇰🇷", layout="centered")

# ==========================================
# 2. 極簡深色 CSS
# ==========================================
st.markdown("""
    <style>
    /* 全局設定：純黑背景 */
    .stApp { background-color: #000000 !important; }
    
    /* 文字顏色：全白 */
    h1, h2, h3, h4, p, span, div, label { 
        color: #FFFFFF !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
    }
    
    /* 卡片風格 */
    div[data-testid="stExpander"], div.stContainer {
        background-color: #1C1C1E;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: none;
    }
    
    /* Tab 分頁美化 */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #000000; 
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1C1C1E;
        border-radius: 8px;
        color: #8E8E93 !important; 
        margin-right: 5px;
        border: none;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3A3A3C;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* 按鈕美化：Naver 綠色 */
    div.stButton > button, a[data-testid="stLinkButton"] {
        background-color: #03C75A !important; /* 改成 Naver 的品牌綠色 */
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        height: 50px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 隱藏 Plotly 工具列 */
    .modebar { display: none !important; }
    
    /* 分隔線顏色 */
    hr { border-color: #333333; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 功能函式庫
# ==========================================

# 產生 Naver Map 搜尋連結
def get_naver_map_link(k_name, name):
    # 優先使用韓文名稱搜尋，準確度最高
    query = k_name if k_name else name
    encoded_query = urllib.parse.quote(query)
    # Naver Map 網頁版搜尋連結
    return f"https://map.naver.com/p/search/{encoded_query}"

@st.cache_data(ttl=3600)
def get_hourly_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&timezone=Asia%2FTokyo&start_date=2025-12-05&end_date=2025-12-07"
        r = requests.get(url).json()
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
    target_date = pd.to_datetime(target_date_str).date()
    day_df = df[df['time'].dt.date == target_date].copy()
    day_df = day_df[(day_df['time'].dt.hour >= 8) & (day_df['time'].dt.hour <= 23)] 
    
    if day_df.empty: return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=day_df['time'], y=day_df['temp'],
        mode='lines+text',
        line=dict(color='#03C75A', width=3), # 線條也改成 Naver 綠
        fill='tozeroy',
        fillcolor='rgba(3, 199, 90, 0.1)',
        text=[f"{t:.0f}°" for t in day_df['temp']],
        textposition="top center",
        textfont=dict(color='white', size=12)
    ))

    fig.update_layout(
        title=dict(text=f"🌡️ {target_date_str[5:]} 氣溫走勢", font=dict(color="white", size=14)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        height=180,
        showlegend=False,
        xaxis=dict(showgrid=False, tickformat='%H', tickfont=dict(color='#888'), dtick=10800000.0),
        yaxis=dict(showgrid=False, visible=False, range=[day_df['temp'].min()-2, day_df['temp'].max()+4])
    )
    return fig

# ==========================================
# 4. 行程資料 (新增 k_name 韓文名稱)
# ==========================================
itinerary = {
    "12/5 (Day 1)": {
        "date": "2025-12-05",
        "items": [
            {
                "time": "15:00", "title": "✈️ 抵達/Check-in", 
                "desc": "機場快線 AREX 直達弘大，先去飯店放行李", 
                "transport": "AREX 機場快線", "k_name": "홍대입구역", "loc": "Hongik Univ. Station"
            },
            {
                "time": "18:00", "title": "🍽 小豬存錢筒", 
                "desc": "弘大必吃石頭烤肉，石頭上烤的豬五花", 
                "transport": "步行前往", "k_name": "돼지저금통", "loc": "Piggy Bank Stone Grill"
            },
            {
                "time": "20:00", "title": "🛍 弘大商圈", 
                "desc": "街頭表演、美妝、買衣服、拍貼機", 
                "transport": "步行", "k_name": "홍대거리", "loc": "Hongdae Street"
            }
        ]
    },
    "12/6 (Day 2)": {
        "date": "2025-12-06",
        "items": [
            {
                "time": "11:00", "title": "🥩 馬場洞韓牛", 
                "desc": "頂級 1++ 韓牛，入口即化 (推薦龍門家)", 
                "transport": "5號線 馬場站 2號出口", "k_name": "마장축산물시장", "loc": "Majang Meat Market"
            },
            {
                "time": "14:00", "title": "📷 證件照拍攝", 
                "desc": "韓式精修證件照，記得帶妝", 
                "transport": "地鐵移動", "k_name": "사진관", "loc": "Photostudio" # 通用搜尋
            },
            {
                "time": "15:30", "title": "🛍 龍山 I’Park", 
                "desc": "超大購物中心，有龍貓展、相機街", 
                "transport": "1號線 龍山站", "k_name": "용산 아이파크몰", "loc": "I'Park Mall"
            },
            {
                "time": "18:30", "title": "🍲 一隻雞 (晚餐)", 
                "desc": "陳玉華或孔陵，蒜味濃郁雞湯", 
                "transport": "4號線 東大門站", "k_name": "진옥화할매원조닭한마리", "loc": "Jin Ok-hwa Halmae"
            },
            {
                "time": "20:30", "title": "🍸 梨泰院酒吧", 
                "desc": "Fountain / Thursday Party，異國風情夜生活", 
                "transport": "6號線 梨泰院站", "k_name": "이태원거리", "loc": "Itaewon Street"
            }
        ]
    },
    "12/7 (Day 3)": {
        "date": "2025-12-07",
        "items": [
            {
                "time": "10:30", "title": "🐷 金豬食堂", 
                "desc": "米其林推薦，最好吃的烤豬頸肉 (需排隊)", 
                "transport": "3號線 藥水站", "k_name": "금돼지식당", "loc": "Gold Pig Dining"
            },
            {
                "time": "13:30", "title": "🛍 明洞商圈", 
                "desc": "Olive Young 旗艦店、明洞聖堂", 
                "transport": "4號線 明洞站", "k_name": "명동거리", "loc": "Myeongdong Street"
            },
            {
                "time": "18:00", "title": "🍽 無垢屋", 
                "desc": "清淡牛肉湯 (Gomguk)，舒緩腸胃", 
                "transport": "1號線 市廳站", "k_name": "무구옥", "loc": "Muguok"
            }
        ]
    }
}

backup_plans = [
    {"name": "Coex 星空圖書館", "desc": "室內雨天備案，絕美書牆", "k_name": "별마당도서관"},
    {"name": "漢南洞", "desc": "設計師品牌聚集地", "k_name": "한남동카페거리"},
    {"name": "樂天超市 (首爾站)", "desc": "伴手禮採買", "k_name": "롯데마트 서울역점"}
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
    st.markdown(f"<p style='color:#03C75A !important; font-weight:bold;'>🚀 距離出發還有 {days_left} 天</p>", unsafe_allow_html=True)

# 抓取天氣資料
weather_df = get_hourly_weather()

st.markdown("---")

# 建立分頁
tab1, tab2, tab3, tab_money, tab_backup = st.tabs(["Day 1", "Day 2", "Day 3", "💰 分帳", "備案"])

# --- 通用渲染函數 (Naver Map 版) ---
def render_day_tab(day_key):
    day_data = itinerary[day_key]
    date_str = day_data['date']
    
    # 天氣圖表
    if weather_df is not None:
        fig = plot_weather_chart(weather_df, date_str)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # 行程列表
    for item in day_data['items']:
        with st.container():
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{item['title']}**")
            col2.markdown(f"*{item['time']}*")
            
            st.caption(item['desc'])
            
            b1, b2 = st.columns([3, 2])
            b1.markdown(f"🚇 {item['transport']}")
            
            # 使用 Naver Map 連結，優先使用韓文名稱搜尋
            map_url = get_naver_map_link(item.get('k_name'), item['loc'])
            b2.link_button("📍 Naver Map", map_url, use_container_width=True)

with tab1: render_day_tab("12/5 (Day 1)")
with tab2: render_day_tab("12/6 (Day 2)")
with tab3: render_day_tab("12/7 (Day 3)")

# --- 💰 分帳功能 (Line 導流版) ---
with tab_money:
    st.subheader("💸 旅費管理")
    st.info("點擊下方按鈕前往 Line 群組記帳")
    
    st.link_button("🚀 開啟 Line 分帳群組", "https://liff.line.me/1655320992-Y8GowEpw/g/pEHGMZAzu5UAyZXX4F268P")
    
    st.caption("建議使用 Splitwise 或 Line 內建分帳功能")

# --- 備案 ---
with tab_backup:
    for plan in backup_plans:
        st.markdown(f"**📍 {plan['name']}**")
        st.caption(plan['desc'])
        
        # 備案也要 Naver Map
        map_url = get_naver_map_link(plan.get('k_name'), plan['name'])
        st.link_button("📍 Naver Map", map_url)
        st.divider()

# Footer
st.caption("2025 Seoul Trip | Naver Map Edition")
