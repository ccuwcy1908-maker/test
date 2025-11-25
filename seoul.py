import streamlit as st
import pandas as pd

# 設定頁面資訊
st.set_page_config(page_title="🇰🇷 首爾三日遊 & 分帳", page_icon="✈️")

# --- 側邊欄：導航 ---
st.sidebar.title("🇰🇷 首爾行導航")
page = st.sidebar.radio("前往功能", ["📅 行程表", "💰 分帳計算機"])

# --- 資料：行程內容 ---
itinerary = {
    "12/5 (Day 1)": [
        {"time": "✈️ 抵達", "activity": "抵達首爾 / Check-in", "note": "記得買 T-Money 卡"},
        {"time": "18:00", "activity": "🍽 晚餐：小豬存錢筒 (돼지저금통)", "note": "📍 弘大附近 | 主打石頭烤肉"},
        {"time": "20:00", "activity": "🌙 自由活動 / 休息", "note": "第一天保留體力"}
    ],
    "12/6 (Day 2)": [
        {"time": "11:00", "activity": "🥩 早午餐：馬場洞韓牛", "note": "📍 馬場畜產物市場 | 買肉上2樓烤"},
        {"time": "14:00", "activity": "📷 證件照拍攝", "note": "📍 需提前預約"},
        {"time": "15:30", "activity": "🛍 逛街：龍山 I’Park Mall", "note": "電子產品、百貨"},
        {"time": "18:30", "activity": "🍲 晚餐：陳玉華/孔陵一隻雞", "note": "熱湯補身"},
        {"time": "20:30", "activity": "🍸 酒吧：梨泰院", "note": "Pistil / Fountain / Thursday Party"}
    ],
    "12/7 (Day 3)": [
        {"time": "10:30", "activity": "🐷 排隊：金豬食堂 (금돼지식당)", "note": "📍 米其林推薦 | 預計排 1 小時"},
        {"time": "13:30", "activity": "🛍 逛街：明洞商圈", "note": "Olive Young 旗艦店、明洞聖堂"},
        {"time": "18:00", "activity": "🍽 晚餐：無垢屋 (무구옥)", "note": "📍 清淡牛肉湯、烤肉"}
    ]
}

# --- 功能 1：行程表 ---
if page == "📅 行程表":
    st.title("🇰🇷 韓國三日行程表")
    
    # 使用 Tabs 切換日期
    tab1, tab2, tab3 = st.tabs(["12/5 (Day 1)", "12/6 (Day 2)", "12/7 (Day 3)"])
    
    def show_day(day_key):
        for item in itinerary[day_key]:
            with st.expander(f"{item['time']} - {item['activity']}", expanded=True):
                st.write(f"💡 {item['note']}")
                st.checkbox("已完成", key=item['activity'])

    with tab1:
        show_day("12/5 (Day 1)")
    with tab2:
        show_day("12/6 (Day 2)")
    with tab3:
        show_day("12/7 (Day 3)")
        
    st.info("💡 點擊「已完成」可標記行程進度")

# --- 功能 2：分帳計算機 ---
elif page == "💰 分帳計算機":
    st.title("💸 旅費分帳助手")

    # 初始化 Session State 來儲存帳目
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []

    # 輸入區
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        item_name = col1.text_input("消費項目 (如：金豬食堂)")
        payer = col2.selectbox("誰付錢？", ["我", "旅伴A", "旅伴B", "旅伴C"])
        amount = st.number_input("金額 (韓元 KRW)", min_value=0, step=1000)
        split_by = st.multiselect("誰要分擔？", ["我", "旅伴A", "旅伴B", "旅伴C"], default=["我", "旅伴A", "旅伴B", "旅伴C"])
        
        submitted = st.form_submit_button("➕ 新增這筆消費")

        if submitted and amount > 0 and split_by:
            per_person = amount / len(split_by)
            st.session_state.expenses.append({
                "項目": item_name,
                "付款人": payer,
                "總金額": amount,
                "分擔人數": len(split_by),
                "每人應付": per_person,
                "分擔者": ", ".join(split_by)
            })
            st.success(f"已新增：{item_name} (₩{amount:,})")

    # 顯示帳目表
    if st.session_state.expenses:
        st.divider()
        st.subheader("📊 消費列表")
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df)

        # 簡單結算邏輯 (示意)
        total_spent = df["總金額"].sum()
        st.metric(label="總消費 (KRW)", value=f"₩{total_spent:,}")
        
        if st.button("🗑 清除所有帳目"):
            st.session_state.expenses = []
            st.rerun()
