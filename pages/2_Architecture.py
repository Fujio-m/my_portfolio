import streamlit as st

st.title("🏗️ システム構成図")

st.header("1. システム全体像")
# 構成図の画像がある場合は以下をアンコメント
# st.image("assets/system_diagram.png", caption="システム構成図")

st.markdown("""
本システムは、**RAG (Retrieval-Augmented Generation)** という手法を用いて、
特定のドキュメント（就業規則等）に基づいた回答を生成します。

### 🛠️ 技術スタック
- **Frontend/Backend:** Streamlit (Python)
- **AI Model:** gemini-2.5-flash-lite
- **API:** Google AI Studio API
- **Data Source:** PDFファイル（社内規定、勤怠マニュアル）
""")

with st.expander("🔍 処理の流れを見る"):
    # ステータス表示（実際の処理ではないので、静的に表示）
    st.write("AIが回答を生成するまでのプロセス：")
    
    with st.status("処理ステップの詳細", expanded=True):
        st.write("1. 📥 ユーザーの質問を受付")
        st.write("2. 📄 PDF内から関連セクションを抽出 (Retrieval)")
        st.write("3. 🧠 Gemini APIへコンテキストを送信")
        st.write("4. ✨ 根拠に基づいた回答を出力 (Generation)")