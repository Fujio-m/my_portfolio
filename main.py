import streamlit as st

# main.py
#
#【プロジェクト概要とナビゲーション設計】
#  本プロジェクトは、実務における「就業規則の参照コスト削減」と「自己解決率の向上」を目的とした
#  RAG（検索拡張生成）チャットボットのポートフォリオです。
#
# 【設計の柱】
#  1. RAGによる就業規則の自動回答（利便性と正確性の向上）
#  2. 実務を見据えたセキュリティ設計（機密情報の分離・非学習環境）
#  3. 疎結合なナビゲーション構造（st.navigationによる各機能の独立）

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
    "システム概要と精度評価": [
        st.Page("pages/2_Architecture.py", title="システム構成図", icon="🏗️"),
        st.Page("pages/4_Evaluation.py", title="精度評価・テスト", icon="🧪"),
        st.Page("pages/5_Operation.py", title="PDF更新サイクル", icon="🔄"),
    ],
    "アプリケーション本体":[
        st.Page("pages/3_Chatbot.py", title="AIチャットボット", icon="🤖")
    ]
})

pg.run()
