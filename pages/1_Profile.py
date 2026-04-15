import streamlit as st
from utils.responsive import inject_responsive_css, responsive_title, responsive_header

# 1_Profile.py - プロフィール & 保有資格
#
# 【設計意図】
# 自身の「自己紹介」と「保有資格」を表示することを目的とする

def main():
    inject_responsive_css()
    responsive_title("👤 自己紹介")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        responsive_header("基本情報")
        st.write("名前: Fujio-m(GitHub名)")
        st.write("年齢: 34歳")
        st.write("目標・キャリアビジョン")
        st.info("""
            **ユーザーの問題を解決できる人材になるために**

            AIの活用や業務自動化を通じて、チームの方々の生産性向上に貢献を目指しています。

            開発スキルに加え、最新の生成AIと実務効率化の視点を掛け合わせ、
            「小さなストレスを解消して業務に集中できる環境」を目指したいと考えています。
            """)

    with col2:
        responsive_header("保有資格")

        with st.expander("🌐 クラウド・AI関連", expanded=True):
            st.write("- Azure AZ-900 / DP-900 / AI-900")
            st.write("- Microsoft PL-900")
            st.write("- Google Cloud Generative AI Leader")

        with st.expander("🐍 開発・共通基盤"):
            st.write("- 基本情報技術者")
            st.write("- ITパスポート")
            st.write("- Python 3 エンジニア認定 (基礎・データ分析)")
            st.write("- Oracle Java SE Bronze")

        with st.expander("📊 ビジネス・Office"):
            st.write("- MOS Expert (Excel, Word)")
            st.write("- MOS PowerPoint")

if __name__ == "__main__":
    main()
