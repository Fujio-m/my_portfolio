import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import os

# ---  メソッド定義 (UIパーツ) ---
def display_faq_buttons():
    """挨拶メッセージ直下のFAQボタンを表示し、選択された質問を返す"""
    st.caption("💡 よくある質問例：")
    # 縦に並べる。keyを固定することで、再実行されてもボタンの状態が維持されます。
    if st.button("🕒 時差出勤の昼休憩の時間は？", key="btn_faq_1"):
        return "時差出勤の昼休憩の時間は？"
    if st.button("📝 時差出勤の申請ルール", key="btn_faq_2"):
        return "時差出勤のルールは？"
    if st.button("🆘 急に休みたくなった時は？", key="btn_faq_3"):
        return "急に休みたくなった時は？"
    if st.button("🚃 電車が遅延した場合は？", key="btn_faq_4"):
        return "電車が遅延した場合は？"
    return None

def display_feedback_buttons(idx):
    """AI回答の下に解決ボタンを縦並びで表示し、ステータスを管理する"""
    # まだ未回答ならボタンを表示
    st.divider()
    st.write("💡 **解決しましたか？**")

    if st.button("👍 はい (解決した)", key=f"yes_{idx}"):
        return "解決しました"
    if st.button("👎 いいえ (解決しない)", key=f"no_{idx}"):
        return "解決してません"
    return None

# --- メソッド定義 (データ処理・API) ---
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

# --- 3. メイン処理 ---
# PDFの準備（パスはご自身の環境に合わせてください）
pdf_path = "data/kintai_rule.pdf"

if os.path.exists(pdf_path):
    pdf_content = get_pdf_text(pdf_path)
    client = get_ai_client()

    # --- 2. 画面表示とボタンの配置 ---
    selected_question = None
    feedback_selection = None

    for i, msg in enumerate(st.session_state.display_history):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # 「最初のメッセージ（i=0）」の時だけ、その枠内にボタンを表示する
            if i == 0:
                selected_question = display_faq_buttons()

            # 最新のアシスタントの回答の場合のみ表示
            if msg["role"] == "assistant" and i == len(st.session_state.display_history) - 1:
                # 🌟 追加：解決後の挨拶メッセージにはボタンを出さない判定
                is_not_feedback_reply = "光栄です" not in msg["content"] and "申し訳ありません" not in msg["content"]

                if i > 0 and is_not_feedback_reply:
                    feedback_selection = display_feedback_buttons(i)

    # --- 入力エリア ---
    chat_prompt = st.chat_input("勤怠について質問してください")
    final_prompt = None
    if selected_question:
        final_prompt = selected_question
    elif feedback_selection:
        final_prompt = feedback_selection
    else:
        final_prompt = chat_prompt

    # --- 回答生成プロセス ---
    if final_prompt:
        # 履歴（表示用）に追加して画面に表示
        st.session_state.display_history.append({"role": "user", "content": final_prompt})
        with st.chat_message("user"):
            st.markdown(final_prompt)

        if final_prompt in ["解決しました", "解決してません"]:
            with st.chat_message("assistant"):
                if final_prompt == "解決しました":
                    msg = "お役に立てて光栄です！また何かあればいつでもご質問ください。"
                    st.success(msg)
                else:
                    form_url = st.secrets["FORM_URL"]
                    msg = f"お役に立てず申し訳ありません。詳細な状況を添えて、[こちらの問い合わせフォーム]({form_url})への相談をご検討ください。"
                    st.info(msg)
                
                # リロードしてもメッセージが残り、ボタンは消えます
            st.session_state.display_history.append({"role": "assistant", "content": msg})
            st.rerun()

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

                    # 4.次回の会話のために履歴に蓄積
                    st.session_state.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=final_prompt)]))
                    st.session_state.chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ans_text)]))
                    st.session_state.display_history.append({"role": "assistant", "content": ans_text})
                    st.rerun()

                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ API制限がかかりました。1分ほど待ってから再度お試しください。")
                    elif "503" in str(e):
                        st.error("☁️ 現在Googleのサーバーが大変混み合っています。少し時間をおいてから再度お試しください。")
                    else:
                        st.error(f"エラーが発生しました: {e}")
else:
    st.error("PDFファイルが見つかりません。dataフォルダを確認してください。")