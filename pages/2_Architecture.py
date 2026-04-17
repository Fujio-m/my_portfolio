import streamlit as st
import os
from utils.json_loader import get_url
from utils.responsive import inject_responsive_css, responsive_title, responsive_header


# 2_Architecture.py - 設計思想とシステム構造
#
# 【設計意図】
# 本ページでは、本アプリの「設計思想とシステム構造」を可視化しています。
# 処理フローの全体像（シーケンス図）に加え、各技術の選定理由や、
# セキュリティ・運用性を重視した設計のこだわりを体系的に提示することを目的とする。


def main():
    inject_responsive_css()
    responsive_title("システム構成図 & 技術スタック")
    st.markdown("""
    本アプリケーションのチャットボットの構成図と使用した技術スタックについて解説します。
    """)

    st.divider()
    responsive_header("1. チャットボットのシーケンス図 ")

    # 画像のパスと使用ツールのURL
    IMAGE_PATH = os.path.join("assets", "chatbot_sequence.png")
    MERMAID_URL = get_url("mermaid_url")

    # 画像が存在する場合のみ表示（エラー防止）
    if os.path.exists(IMAGE_PATH):
        st.image(IMAGE_PATH,
                caption=f"勤怠管理Q&Aチャットボット シーケンス図 【使用ツール:[mermaid]({MERMAID_URL})】",
                width='stretch'
                )

        with st.expander("🔍 図の解説（クリックで展開）"):
            with st.expander("⚙️ 1. 初期化プロセス（システム起動時の準備）", expanded=True):
                st.markdown("""
                アプリが起動した際、バックグラウンドで実行される準備工程です。

                * **APIキーの読み込み・認証情報の返却**:
                    * `.streamlit/secrets.toml` から安全にAPIキーを取得し、外部に漏洩しないように**セキュリティ設計**を徹底しています。
                * **勤怠ルールの読み込み・テキストデータの保持**:
                    * 就業規則PDFからテキストを抽出し、メモリ上に保持。このテキストからAIが質問に対して回答する形になります。
                """)

            with st.expander("💬 2. 対話プロセス（ユーザーとの対話フロー）"):
                st.markdown("""
                利用者が質問を入力してから、回答が表示されるまでの動的な工程です。

                * **質問の入力**:
                    * ユーザーが「午前休の時間は？」等の質問の入力や「よくある質問」からボタンを押下して送信
                * **ユーザー質問  PDF+コンテキストを送信**:
                    * 送信された質問とPDFの内容を「参考情報」としてGemini APIへ送信
                * **生成された回答を返却 & Streamlit UIに表示**:
                    * **Gemini 2.5 Flash-lite** が最適な回答を生成し、チャット画面上に即座に回答します。
                """)
    else:
        st.error(f"⚠️ 画像ファイルが見つかりません: `{IMAGE_PATH}` に画像を配置してください。")

    st.divider()

    responsive_header("2. 技術スタック & 選定理由")
    responsive_header("🛠️ 使用フレームワーク・ライブラリ")
    st.markdown("""
        | カテゴリ | 技術 | 採用理由 |
        | :--- | :--- | :--- |
        | 開発言語  | Python 3.13.2 | AIライブラリが豊富なため |
        |  フレームワーク | Streamlit 1.55.0 | 素早く簡易的にAIモデル開発ができるため |
        |  AIモデル | Gemini 2.5 Flash-lite| 無料枠で最新かつ低コストで運用が可能なため |
        |  データ可視化 | Plotly | 動的なグラフが表示可能なため |
        |  データ処理 | Pandas | CSVの統計処理に必要なため |
        |   PDF処理  | PyPDF | PDFテキスト抽出機能に必要なため |
        """)

    responsive_header("🛠️ 技術選定の詳細理由")
    col_left, col_right = st.columns(2)
    with col_left:
        st.success("**なぜ Google Gemini (API) なのか？**")
        st.markdown("""
        - **コストパフォーマンスの最適化**:
            - プロトタイプ開発において、AIモデルを低コスト（現在はGoogle AI Studioの無料枠）で運用できるため。
        - **実務移行時の高い安全性**:
            - 現在は無料枠のAPIを使用していますが、実務運用では **Vertex AI Studio** 経由への切り替えを想定。入力データがモデルの学習に利用されない環境を構築し、社外秘である勤怠ルールの情報漏洩を確実に防止するため。
        """)

    with col_right:
        st.success("**なぜ Python / Streamlit なのか？**")
        st.markdown("""
        - **迅速なプロトタイピング**:
            - HTMLなどの作成が必要なく、素早くアプリ構築ができるため
        - **拡張性と柔軟性**:
            - Pythonのライブラリを活用し、将来的なデータ分析機能などの追加などができるため
        """)

    responsive_header("💡 設計におけるこだわりポイント")
    col_1, col_2 = st.columns(2)

    with col_1:
        st.success("**🔐 セキュリティ & 信頼性**")
        st.markdown("""
        - **機密情報の完全分離**
            - `secrets.toml` を活用し、APIキーがGitHub等への流出を徹底防止。
        - **ハルシネーションの抑制**
            - システムプロンプトにて「提供資料外の回答を禁止」し、引用をPDFに限定。AIの憶測での発言を抑えて情報の信頼性を確保。
        - **環境の独立性と再現性**
            - `venv`（仮想環境）と `requirements.txt` により、OSに依存しない安定した動作環境を構築。
        - **プロンプトの外出し管理**
            - システムプロンプトを `.md` ファイルとして分離。システムプロンプトのメンテナンスミスを防止。
        """)

    with col_2:
        st.success("**🏗️ 実務・運用・UX設計**")
        st.markdown("""
        - **エスカレーションフローの統合**
            - AIで解決しない場合、**問い合わせフォーム**へ案内。ユーザーの「未解決」を放置しない設計。
        - **導入コストを最小化するUX設計**
            - **使い方ガイド**: 別途マニュアルを開く手間を省き、初見のユーザーでも操作できる画面設計。
            - **よくある質問のボタン実装**: よくある質問をボタンですぐに質問できるようにしてユーザーの問い合わせ時間の低減
        - **管理者の更新作業の負担低減**
            - 勤怠ルールPDFを差し替えるだけで最新の規定をAIが即座に学習。「プログラム改修コストなし」の持続可能な運用モデル。
        """)

if __name__ == "__main__":
    main()