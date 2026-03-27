import streamlit as st

def main():
    st.title("👤 自己紹介")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("基本情報")
        st.write("名前: Fujio-m(GitHub名)")
        st.write("年齢: 34歳")
        st.write("目標・キャリアビジョン")
        st.info("""
            **IT技術による「現場の課題解決」のスペシャリストへ**

            AI利活用や業務自動化を通じて、組織の生産性向上に直結する貢献を目指しています。

            開発スキルに加え、最新の生成AI知見と実務効率化の視点を掛け合わせ、
            「社員がよりクリエイティブな仕事に集中できる環境」を構築したいと考えています。
            """)

    with col2:
        st.subheader("保有資格")
        
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
