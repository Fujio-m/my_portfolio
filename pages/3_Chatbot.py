import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import os

# --- 1. ページ設定とUI ---
st.set_page_config(page_title="勤怠管理QAボット", layout="wide")
st.title("🤖 勤怠管理QAアシスタント")

# セッションステート（履歴保存用）の初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 表示用履歴の初期化（ここに最初の挨拶を入れる）
if "display_history" not in st.session_state:
    initial_message =(
        "こんにちは。 社内規定（勤怠管理）について、どのような情報をお探しでしょうか？\n\n"
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

    # --- 2. 画面表示とボタンの配置 ---
    selected_question = None

    for i, msg in enumerate(st.session_state.display_history):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

        # 「最初のメッセージ（i=0）」の時だけ、その枠内にボタンを表示する
        # 条件を i == 0 だけにすることで、会話が進んでも「最初の挨拶の下」にボタンが残り続けます
        if i == 0:
            st.caption("💡 よくある質問例：")
            # 縦に並べる。keyを固定することで、再実行されてもボタンの状態が維持されます。
            if st.button("🕒 時差出勤の昼休憩の時間は？", key="btn_faq_1"):
                selected_question = "時差出勤の昼休憩の時間は？"
            if st.button("📝 時差出勤の申請ルール", key="btn_faq_2"):
                selected_question = "時差出勤のルールは？"
            if st.button("🆘 急に休みたくなった時は？", key="btn_faq_3"):
                selected_question = "急に休みたくなった時は？"
            if st.button("🚃 電車が遅延した場合は？", key="btn_faq_4"):
                selected_question = "電車が遅延した場合は？"

        # AIの回答（assistant）に対して「解決ボタン」を表示
            if msg["role"] == "assistant" and i > 0:
                st.divider()
                st.write("💡 **解決しましたか？**")
                
                # ボタンのキーを一意にする
                btn_key_id = i 
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 はい", key=f"yes_{btn_key_id}", use_container_width=True):
                        st.session_state[f"status_{btn_key_id}"] = "resolved"
                with col2:
                    if st.button("👎 いいえ", key=f"no_{btn_key_id}", use_container_width=True):
                        st.session_state[f"status_{btn_key_id}"] = "unresolved"

                # 状態のチェックとメッセージ表示
                status = st.session_state.get(f"status_{btn_key_id}")
                if status == "resolved":
                    st.success("ご利用ありがとうございました！")
                elif status == "unresolved":
                    form_url = st.secrets["contact"]["form_url"]
                    esc_msg = st.secrets["contact"]["escalation_msg"]
                    st.info(f"{esc_msg}\n\n👉 [勤怠問い合わせフォーム]({form_url})")
                    st.warning("⚠️ **緊急の場合**は上司へお電話ください。")

    # チャット入力
    chat_prompt = st.chat_input("勤怠について質問してください")

    # ボタンが押されたか、チャットが入力されたかを判定
    final_prompt = selected_question if selected_question else chat_prompt

    # 何かしらの入力があった場合に実行
    if final_prompt:
        # 履歴（表示用）に追加して画面に表示
        st.session_state.display_history.append({"role": "user", "content": final_prompt})
        with st.chat_message("user"):
            st.markdown(final_prompt)

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
                        contents=st.session_state.chat_history + [final_prompt], # 履歴 + 今回の質問
                        config=types.GenerateContentConfig(
                            system_instruction=final_instruction,
                            temperature=0.1,
                        )
                    )

                    # 3. 結果を画面表示 & 履歴（保存用）に追加
                    ans_text = response.text
                    st.markdown(ans_text)


                    # 次回の会話のために履歴に蓄積
                    st.session_state.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=final_prompt)]))
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