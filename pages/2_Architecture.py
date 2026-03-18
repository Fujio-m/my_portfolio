import streamlit as st
import os

def main():
    # ページ設定（ブラウザのタブに表示される名前とアイコン）
    st.set_page_config(page_title="システム構成 | AI勤怠管理Q&A", page_icon="🏗️", layout="wide")

    # タイトルと導入文
    st.title("🏗️ システム構成図 & 技術スタック")
    st.markdown("""
    本アプリケーションのデータフロー、コンポーネント間の連携、および採用している技術スタックについて解説します。
    実務での運用を想定し、セキュリティ(認証情報の隠蔽)と最新のAI技術(RAG)を組み合わせた設計を行っています。
    """)

    st.divider() # 区切り線

    # --- セクション1: システム構成図 ---
    st.header("1. チャットボットのデータフロー図 ")

    # 画像のパス（assetsフォルダ内）
    IMAGE_PATH = os.path.join("assets", "chatbot_data_flow.png")

    # 画像が存在する場合のみ表示（エラー防止）
    if os.path.exists(IMAGE_PATH):
        # use_container_width=True で横幅いっぱいに綺麗に表示
        st.image(IMAGE_PATH,
                caption="勤怠管理Q&Aチャットボット シーケンス図", 
                use_container_width=True)

        with st.expander("🔍 図の解説（クリックで展開）"):
            st.markdown("""
            この図は、ユーザーの質問がどのように処理されるかを示しています。
            1.  **認証**: アプリ起動時に、GitHubに公開されない `.streamlit/secrets.toml` からAPIキーを安全に読み込みます。
            2.  **RAG (Retrieval-Augmented Generation)**: 質問に関連するPDFテキストを抽出し、システムプロンプトと共にGemini APIへ送信します。これにより、AIの「知ったかぶり（ハルシネーション）」を防ぎ、正確な回答を実現します。
            """)
    else:
        st.error(f"⚠️ 画像ファイルが見つかりません: `{IMAGE_PATH}` に画像を配置してください。")

    st.divider()

    # --- セクション2: 技術スタック ---
    st.header("2. 技術スタック & 選定理由")

    # 2カラム構成にする
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛠️ 使用フレームワーク・ライブラリ")
        st.markdown("""
        -   **Language**: Python 3.13.2
        -   **Web Framework**: **Streamlit 1.55.0**
            -   （選定理由: 高速なプロトタイピングと、直感的なUI構築が可能なため）
        -   **AI Engine**: **Gemini 2.5 Flash-lite** (`google-genai 1.67.0`)
            -   （選定理由: PDFのコンテキスト注入に優れ、高速かつ安価に動作するため。）
        -   **PDF Processing**: **pypdf 6.9.0**
            -   （選定理由: 純Python製で依存が少なく、安定してテキスト抽出を行えるため）
        """)

    with col2:
        st.subheader("💡 設計におけるこだわりポイント")
        # 資格と結びつけたアピール
        st.info("""
        **【セキュリティ & メンテナンス性】**
        -   **APIキーの隠蔽**: `.gitignore` を適切に設定し、機密情報を GitHub に流出させない実務的な設計
        -   **環境の再現性**: `requirements.txt` にライブラリのバージョンを明記し、誰でも同じ環境を構築可能に

        **【AI精度の向上 (RAG)】**
        -   ただチャットするだけでなく、社内規定PDFをコンテキストとして与えることで、正確な回答を導く設計
        """)

if __name__ == "__main__":
    main()