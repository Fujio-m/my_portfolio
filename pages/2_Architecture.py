import streamlit as st
import os

def main():
    # ページ設定（ブラウザのタブに表示される名前とアイコン）
    st.set_page_config(page_title="システム構成 | AI勤怠管理Q&A", page_icon="🏗️", layout="wide")

    # タイトルと導入文
    st.title("🏗️ システム構成図 & 技術スタック")
    st.markdown("""
    * 本アプリケーションのデータフロー、コンポーネント間の連携、および採用している技術スタックについて解説します。
    * 実務での運用を想定し、セキュリティ(認証情報の隠蔽)と最新のAI技術(RAG)を組み合わせた設計を行っています。
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
            # 1. 初期化プロセスの解説
            with st.expander("⚙️ 1. 初期化プロセス（システム起動時の準備）", expanded=True):
                st.markdown("""
                アプリが起動した際、バックグラウンドで実行される準備工程です。
    
                * **APIキーの読み込み・認証情報の返却**:
                `.streamlit/secrets.toml` から安全に認証情報を取得。ソースコードに機密情報を残さない**セキュリティ設計**を徹底しています。
                * **勤怠ルールの読み込み・テキストデータの保持**:
                規定PDFからテキストを抽出し、メモリ上に保持。これがAIの回答の「根拠」となる**ナレッジベース**となります。
                """)

            # 2. 対話プロセスの解説
            with st.expander("💬 2. 対話プロセス（ユーザーとの対話フロー）"):
                st.markdown("""
                利用者が質問を入力してから、回答が表示されるまでの動的な工程です。
    
                * **質問の入力**:
                ユーザーが「午前休の時間は？」等の疑問を自然言語で入力。直感的なUIで**自己解決**を促します。
                * **ユーザー質問  PDF+コンテキストを送信**:
                質問にPDFの内容を「参考情報」として添えてGemini APIへ送信。社内規定に特化した **根拠ある回答(RAG)** を実現します。
                * **生成された回答を返却 & Streamlit UIに表示**:
                最新の **Gemini 2.3 Flash-lite** が最適な回答を生成し、チャット画面上に即座にフィードバックします。
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