import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. PDF抽出関数（キャッシュ化） ---
@st.cache_data # 一度読み込んだら、ファイルが変わらない限り再実行しません
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"PDF読み込みエラー: {e}")
        return ""

# --- 2. モデル初期化関数（キャッシュ化） ---
@st.cache_resource # モデルの設定自体を使い回すことで、APIへの無駄なリクエストを減らします
def get_gemini_model(pdf_text):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    base_instruction = st.secrets["SYSTEM_INSTRUCTION"]
    final_instruction = base_instruction.replace("{{PDF_CONTENT}}", pdf_text)

    return genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        system_instruction=final_instruction
    )

# --- 実行フェーズ ---

# PDFテキストの取得（キャッシュから読み込まれる）
pdf_content = extract_text_from_pdf("data/kintai_rule.pdf")

# モデルの取得（キャッシュから読み込まれる）
model = get_gemini_model(pdf_content)

# --- 3. 画面（UI）の構築 ---
st.title("🤖 勤怠管理QAアシスタント")
# --- 使い方ガイドのポップアップ ---
with st.popover("📖 このチャットボットの使い方"):
    st.markdown("""
    ### 🤖 勤怠管理Q&Aアシスタントの使い方
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

st.caption("社内規定PDFに基づいて回答します（節約モード稼働中）")

if prompt := st.chat_input("質問をどうぞ"):

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("確認中..."):
            try:
                # generate_content はキャッシュできない（毎回答えが違うため）が、
                # モデル作成がキャッシュされているので、これだけでAPI負荷は激減します。
                response = model.generate_content(prompt)

                if response.candidates and response.candidates[0].content.parts:
                    st.markdown(response.text)
                else:
                    st.warning("AIが回答を生成できませんでした。")

            except Exception as e:
                # 429エラーが出た場合のアドバイスを表示
                if "429" in str(e):
                    st.error("現在APIの利用制限がかかっています。1分ほど待ってから再度お試しください。")
                else:
                    st.error(f"エラーが発生しました: {e}")