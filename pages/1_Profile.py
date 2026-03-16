import streamlit as st

st.title("👤 自己紹介")

col1, col2 = st.columns([1, 2])

with col1:
    # st.image("your_photo.png") # 写真があれば
    st.subheader("基本情報")
    st.write("名前: [あなたの名前]")
    st.write("年齢: 34歳")
    st.write("目標: ITエンジニアとして業務効率化に貢献する")

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
        st.write("- MOS Expert (Excel, Word, PowerPoint)")