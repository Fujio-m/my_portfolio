import streamlit as st

# ナビゲーションの定義
pg = st.navigation([
    st.Page("pages/0_Home.py", title="ホーム", icon="🏠", default=True),
    st.Page("pages/1_Profile.py", title="自己紹介", icon="👤"),
    st.Page("pages/2_Architecture.py", title="システム構成図", icon="🏗️"),
    st.Page("pages/3_Chatbot.py", title="AIチャットボット", icon="🤖"),
])

pg.run()
