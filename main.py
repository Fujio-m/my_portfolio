import streamlit as st

# アプリのページ設定
st.set_page_config(
    page_title="勤怠管理AIポートフォリオ",
    layout="wide",
    page_icon="💼"
)

# ナビゲーションの定義
pg = st.navigation({
    "メインメニュー": [
        st.Page("pages/0_Home.py", title="ホーム", icon="🏠", default=True),
        st.Page("pages/1_Profile.py", title="自己紹介", icon="👤")
    ],
    "プロジェクト": [
        st.Page("pages/2_Architecture.py", title="システム構成図", icon="🏗️"),
        st.Page("pages/3_Chatbot.py", title="AIチャットボット", icon="🤖"),
        st.Page("pages/4_Evaluation.py", title="精度評価・テスト", icon="🧪"),
    ]
})

pg.run()
