import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import os

# --- 1. ページ設定とUI ---
st.set_page_config(page_title="勤怠管理QAボット")
st.title("🤖 勤怠管理QAアシスタント")

# セッションステート（履歴保存用）の初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 表示用履歴の初期化（ここに最初の挨拶を入れる）
if "display_history" not in st.session_state:
    initial_message =(
        "こんにちは。 社内規定（勤怠管理）について、どのような情報をお探しでしょうか？\n\n"
        "例えば、以下のようなご質問にお答えできます。\n"
        "* **[午前休の出勤時間は？]**\n"
        "* **[時差出勤の申請ルール]**\n"
        "* **[急に休みたくなった時は？]**\n"
        "* **[電車が遅延した！]**\n\n"
        "お気軽にご質問ください。"
    )
    
    st.session_state.display_history = [
        {"role": "assistant", "content": initial_message}
    ]

# 使い方ガイド（Popover）
with st.popover("📖 使い方ガイド"):
    st.markdown("""
    #### 🤖 勤怠管理Q&Aアシスタントの使い方
    このボットは社内規定PDFの内容に基づいて、あなたの質問に回答します。

    **【できること】**
    * 勤務時間や休憩時間、休暇（有給・午前休・午後休）のルールや期限の確認
    * 遅刻・早退時の連絡方法の確認
    * 電車遅延やPC故障などの緊急時の対応ガイド

    **【使い方のコツ】**
    * 「午前休は何時まで？」のように具体的に聞いてください。
    * PDFに記載がない事項については、AIがその旨を回答します。

    ---
    ⚠️ **注意点**
    * 1分間に何度も質問すると、APIの制限によりエラー（429）が出ることがあります。その場合は1分ほど待ってから再度入力してください。
    """)

st.divider()

# --- 2. PDF読み込みとクライアント初期化（キャッシュ化） ---
@st.cache_resource
def get_pdf_text(pdf_path):
    """PDFからテキストを抽出してキャッシュする"""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

@st.cache_resource
def get_ai_client():
    """最新のGoogle Gen AIクライアントを初期化"""
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- 3. メイン処理 ---
# PDFの準備（パスはご自身の環境に合わせてください）
pdf_path = "data/kintai_rule.pdf"

if os.path.exists(pdf_path):
    pdf_content = get_pdf_text(pdf_path)
    client = get_ai_client()

    # 画面にこれまでの会話を表示
    for msg in st.session_state.display_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # チャット入力
    if prompt := st.chat_input("勤怠について質問してください"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # ここにスピナー（ぐるぐる）を追加
            with st.spinner("AIが規定を確認しています..."):
                try:
                    # システムプロンプトの構築
                    base_instruction = st.secrets["SYSTEM_INSTRUCTION"]
                    final_instruction = base_instruction.replace("{{PDF_CONTENT}}", pdf_content)

                    # 最新パッケージでの生成処理
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", # Liteモデルを指定
                        contents=st.session_state.chat_history + [prompt], # 履歴 + 今回の質問
                        config=types.GenerateContentConfig(
                            system_instruction=final_instruction,
                            temperature=0.1,
                        )
                    )
                
                    # 3. 結果を画面表示 & 履歴（保存用）に追加
                    ans_text = response.text
                    st.markdown(ans_text)
                
                    # 次回の会話のために履歴に蓄積
                    st.session_state.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
                    st.session_state.chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ans_text)]))
                    st.session_state.display_history.append({"role": "assistant", "content": ans_text})

                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ API制限がかかりました。1分ほど待ってから再度お試しください。")
                    elif "503" in str(e):
                        st.error("☁️ 現在Googleのサーバーが大変混み合っています。少し時間をおいてから再度お試しください。")
                    else:
                        st.error(f"エラーが発生しました: {e}")
else:
    st.error("PDFファイルが見つかりません。dataフォルダを確認してください。")