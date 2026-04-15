import streamlit as st
from utils.json_loader import get_url
from utils.responsive import inject_responsive_css, responsive_title, responsive_header

# 5_Operation.py - 運用設計 & PDCAサイクル
#
# 【設計意図】
# AIアプリを持続可能な「社内インフラ」として定着させるための運用フローを提示。
# 1. データの鮮度管理（PDF更新）
# 2. ユーザーフィードバックの収集
# 3. 勤怠ルールPDF更新によるの継続的な問題点の改善
# 以上の3点を可視化し、PDCAサイクルによって「保守・運用意識」をアピールする。

def main():
    inject_responsive_css()
    responsive_title("🔄 未解決質問対策のPDF更新サイクル")
    st.caption("チャットボットが答えられなかった内容を担当者にエスカレーションし改善する設計")

    # --- 導入 ---
    responsive_header("💡 PDF更新によるメリット")
    st.markdown("""
    - **ユーザー** : PDF更新により最新かつ正確な回答が得られる
    - **管理者** : プログラミング不要でルール追加が可能、重複対応の削減
    """)

    # utilsからURLを取得
    BPMN_IO_URL = get_url("bpmn_io_url")

    with st.expander("📊 業務プロセス図を確認", expanded=True):
        st.image("assets/workflow.svg", width='stretch')
        st.caption(f"図：ユーザー・管理者・システムの連携フロー 【使用ツール:[bpmn.io]({BPMN_IO_URL})】")

    st.divider()

    responsive_header("1. 課題の検知とエスカレーション")
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("""
        **【ユーザー視点】**
        - 資料にない質問に対し、AIが無理に答えず「回答不可」と正しく判定

        - 解決しなかった場合に、**問い合わせフォーム**へ案内し、ユーザーの質問を収集します
        """)

    with col2:
        st.image("img/chat_fail.png", caption="図1：ユーザーからの答えられなかった内容", width='stretch')

    st.divider()

    responsive_header("2. 現場の声をデータ化")
    col3, col4 = st.columns([1.5, 1])

    with col3:
        st.image("img/form_submit.png", caption="図2：ユーザーからの具体的な問い合わせ内容", width='stretch')

    with col4:
        st.markdown("""
        **【データ収集】**
        - ユーザーがフォームに入力した質問で知りたかった内容は、Google Formsを通じてリアルタイムで収集できます

        - これにより、ユーザーの解決できなかったことの可視化が可能
        """)

    st.divider()

    responsive_header("3. 管理者による未解決問題の分析")
    col5, col6 = st.columns([1, 1.5])

    with col5:
        st.markdown("""
        **【管理者視点】**
        - 問い合わせされた内容はスプレッドシート等で一元管理

        - 「PDFを更新するだけ」という、**非エンジニアでも勤怠ルールの更新が可能**です
        """)

    with col6:
        st.image("img/spreadsheet.png", caption="図3：管理者用ダッシュボード（課題管理）", width='stretch')

    st.divider()

    responsive_header("4. PDF更新による未解決問題の解決")
    col7, col8 = st.columns([1.5, 1])

    with col7:
        st.image("img/chat_success.png", caption="図4：PDF更新後の回答", width='stretch')

    with col8:
        st.success("✨ **アップデート完了**")
        st.markdown("""
        **【結果】**
        - 管理者がPDFを更新した瞬間にシステムに反映されます

        - PDFが更新された際に同じ質問に対して、今度はチャットボットが回答できるようになります
        """)

    st.info("このPDCAサイクルで新しいルールが追加されたときは答えられなかった内容を改善することでよりユーザーからの問い合わせに対応できるようになります")

if __name__ == "__main__":
    main()