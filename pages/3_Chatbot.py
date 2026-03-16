import streamlit as st
from pypdf import PdfReader

# 1. PDFからテキストを抽出する「道具（関数）」を定義
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        # 全ページをループで回してテキストを取り出す
        for page in reader.pages:
            # ページから文字を抽出。抽出できない場合は空文字を足す
            text += page.extract_text() or ""
        return text
    except FileNotFoundError:
        return "エラー：指定されたPDFファイルが見つかりません。パスを確認してください。"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"

# 画面のタイトル
st.title("Step 1: PDFデータ抽出テスト")

# 2. ファイルパスを指定（dataフォルダの中のファイル名と一致させる）
file_path = "data/kintai_rule.pdf"

# 3. Streamlitのボタンを使って動作確認
if st.button("PDFのテキストを抽出する"):
    with st.spinner("PDFを解析中..."):
        result = extract_text_from_pdf(file_path)
        
        if result:
            st.success("テキストの抽出に成功しました！")
            # 抽出された内容をスクロール可能なエリアに表示
            st.text_area("抽出された内容（プレビュー）", value=result, height=400)
            
            # 文字数を確認（あまりに短い場合は読み取り失敗の可能性があるため）
            st.write(f"抽出された文字数: {len(result)} 文字")
        else:
            st.error("テキストを抽出できませんでした。PDFが画像形式（スキャンしたもの）でないか確認してください。")