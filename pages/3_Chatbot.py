import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
import os

# --- 定数定義 ---
PDF_PATH = "data/kintai_rule.pdf"
GUIDE_PATH = "assets/usage_guide.md"
GEMINI_MODEL = "gemini-2.5-flash-lite"

# ---  メソッド定義 (UIパーツ) ---
@st.cache_data
def load_markdown_file(file_path):
    """Markdownファイルを読み込む関数"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ ガイドファイルが見つかりませんでした。"

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
    try:
        text = ""
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"PDFの解析中にエラーが発生しました:{e}")
        return None

@st.cache_resource
def get_ai_client():
    """最新のGoogle Gen AIクライアントを初期化"""
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def render_chat_interface():
    """チャット履歴と各種ボタンを表示し、ユーザーの選択(FAQ/FB)を返す"""
    selected_question = None
    feedback_selection = None

    for i, msg in enumerate(st.session_state.display_history):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # 最初のみFAQボタンを表示
            if i == 0:
                selected_question = display_faq_buttons()

            # 最新のアシスタントの回答の場合のみ表示
            if msg["role"] == "assistant" and i == len(st.session_state.display_history) - 1:
                # 解決後の挨拶メッセージにはボタンを出さない判定
                is_not_feedback_reply = "光栄です" not in msg["content"] and "申し訳ありません" not in msg["content"]
                if i > 0 and is_not_feedback_reply:
                    feedback_selection = display_feedback_buttons(i)

    return selected_question, feedback_selection

def handle_feedback(final_prompt):
    """解決/未解決ボタンに対するレスポンスを生成し、メッセージを返す"""
    if final_prompt == "解決しました":
        msg = "お役に立てて光栄です！また何かあればいつでもご質問ください。"
        st.success(msg)
    else:
        form_url = st.secrets["FORM_URL"]
        msg = f"お役に立てず申し訳ありません。詳細な状況を添えて、[こちらの問い合わせフォーム]({form_url})への相談をご検討ください。"
        st.info(msg)
    return msg

def get_gemini_answer(client, final_prompt, pdf_content):
    """Gemini APIから回答を取得する"""
    # システムプロンプトの構築
    base_instruction = st.secrets["SYSTEM_INSTRUCTION"]
    final_instruction = base_instruction.replace("{{PDF_CONTENT}}", pdf_content)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=st.session_state.chat_history + [final_prompt], # 履歴 + 今回の質問
            config=types.GenerateContentConfig(
                system_instruction=final_instruction,
                temperature=0.1,
            )
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            st.warning("⚠️ API制限がかかりました。1分ほど待ってから再度お試しください。")    
        elif "503" in str(e):
            st.error("☁️ 現在Googleのサーバーが大変混み合っています。少し時間をおいてから再度お試しください。")
        else:
            st.error(f"エラーが発生しました: {e}")
        return None

def main():
    # --- UI初期設定 ---
    st.set_page_config(page_title="勤怠管理QAボット", layout="wide")
    st.title("🤖 勤怠管理Q&Aチャットボット")

    # セッション状態の初期化
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "display_history" not in st.session_state:
        initial_message =(
            "こんにちは。 社内規定（勤怠管理）について、どのような情報をお探しでしょうか？\n\n"
            "お気軽にご質問ください。"
        )
        st.session_state.display_history = [
            {"role": "assistant", "content": initial_message}
        ]

    # 使い方ガイド表示
    guide_text = load_markdown_file(GUIDE_PATH)
    with st.popover("📖 使い方ガイド"):
        st.markdown(guide_text)
    st.divider()

    # PDFファイルの存在チェック
    if not os.path.exists(PDF_PATH):
        st.error(f"ファイルが見つかりません: {PDF_PATH}")
        return # 処理を中断

    # PDFからテキスト抽出チェック
    pdf_content = get_pdf_text(PDF_PATH)
    if pdf_content is None:
        st.error("規定PDFの読み込みに失敗しました。ファイルが破損しているか、画像のみの可能性があります。")
        return

    # --- インターフェース制御 ---
    client = get_ai_client()

    # --- チャット画面の表示とボタン選択の取得 ---
    selected_question, feedback_selection = render_chat_interface()

    # --- 入力プロンプトの統合と優先順位決定 ---
    chat_prompt = st.chat_input("勤怠について質問してください")
    final_prompt = selected_question or feedback_selection or chat_prompt
    ans_text = None

    # --- 回答生成プロセス ---
    if final_prompt:
        # ユーザー入力の反映
        st.session_state.display_history.append({"role": "user", "content": final_prompt})
        with st.chat_message("user"):
            st.markdown(final_prompt)

        # 入力内容に応じて分岐(フィードバック or AI回答)
        if final_prompt in ["解決しました", "解決してません"]:
            with st.chat_message("assistant"):
                ans_text = handle_feedback(final_prompt)
        else:
            with st.chat_message("assistant"):
                with st.spinner("AIが規定を確認しています..."):
                    ans_text = get_gemini_answer(client, final_prompt, pdf_content)

                    if ans_text:
                        st.markdown(ans_text)
                        # 会話コンテキストを更新
                    st.session_state.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=final_prompt)]))
                    st.session_state.chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ans_text)]))

        # 応答結果の保存と画面の更新
        if ans_text:
            st.session_state.display_history.append({"role": "assistant", "content": ans_text})
            st.rerun()
        else:
            st.error("回答を生成できませんでした。もう一度時間を置いて質問してください。")

if __name__ == "__main__":
    main()