import streamlit as st
from utils.responsive import inject_responsive_css, responsive_title, responsive_header


# 0_Home.py - 開発背景と課題定義
#
# 【設計意図】
#  ポートフォリオのトップ画面として「開発背景」「プロジェクト概要」「解決すべき課題」などを表示する目的とする

def main():
    inject_responsive_css()
    responsive_title("勤怠管理AIチャットボット(ポートフォリオ)")
    st.divider()

    # 開発の動機
    responsive_header("📌 開発の背景と動機")
    st.markdown("""
    私は現在、勤怠管理ツールの担当として、新規入職者からの問い合わせ対応や、ルールの確認・エスカレーション業務に従事しています。

    業務の中で直面した課題を解決するため、本アプリを作成いたしました。

    * **課題**
        * 新規入職者から同じような質問が毎回届き、担当者や上司への確認作業（エスカレーション）で業務負荷が発生している。
    * **狙い**
        * AIチャットボットを活用し、同じような質問などをチャットボットに答えてもらい、担当者の付帯作業時間を削減させる
    """)

    st.divider()

    # プロジェクトの概要
    col1, col2 = st.columns(2)
    with col1:
        responsive_header("💡 プロジェクトについて")
        st.markdown("""
        - 就業規則や勤怠ルールに関する質問に、AIが社内の勤怠ルールPDFに基づいて回答するQ&Aチャットボットです。
        - ユーザーから解決できなかった内容を管理者に問い合わせして勤怠ルールPDFを更新し改善するPDCAサイクルの設計をしています。
        """)

    with col2:
        responsive_header("🌟 解決したい課題")
        st.markdown("""
        - Q&Aチャットボット導入による従業員の自己解決率の向上
        - 管理部門への「同じ質問」を自動化し、対応工数を低減
        - PDF更新だけでチャットボットに反映されるので更新作業負担低減
        """)

    st.divider()

    st.info("👈 左側のサイドメニューから、各機能や詳しいシステム構成をご覧いただけます。")

if __name__ == "__main__":
    main()