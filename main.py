import streamlit as st

# ページの設定
st.set_page_config(page_title="勤怠管理AIチャットボット", layout="wide")

# ナビゲーションの定義
pg = st.navigation([
    st.Page("pages/1_Profile.py", title="自己紹介", icon="👤"),
    st.Page("pages/2_Architecture.py", title="システム構成図", icon="🏗️"),
    st.Page("pages/3_Chatbot.py", title="AIチャットボット", icon="🤖"),
])

# --- メインコンテンツ ---
st.title("💼 勤怠管理AIチャットボットのポートフォリオ")

st.markdown("""
### 💡 このポートフォリオのプロジェクトについて
複雑な就業規則や勤怠ルールに関する質問に、AIがドキュメントに基づいて回答する**RAG（検索拡張生成）システム**を作成いたしました

#### 🌟 解決したい課題
- 管理部門への「同じ質問」の繰り返しを減らし、担当者の対応時間の低減
- 従業員がいつでも即座にルールを確認できる環境を作る

#### 🛠️ 使用技術
- **Frontend:** Streamlit
- **AI Model:** gemini-2.5-flash-lite (Google AI Studio)
- **Method:** RAG (PDFドキュメント参照)
""")

st.info("👈 左側のサイドメニューから、各機能や詳しいシステム構成をご覧いただけます。")

pg.run()
