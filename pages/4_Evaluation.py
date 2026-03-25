import streamlit as st
import pandas as pd
import os

def load_test_data(csv_path):
    """CSVからデータを読み込み、DataFrameを返す"""
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, encoding="utf-8-sig")
    return None

def display_summary_metrics(df):
    """合格率など計算してメトリクスを表示する"""
    total_cases = len(df)
    pass_cases = len(df[df["判定"].str.contains("✅", na=False)])
    pass_rate = (pass_cases / total_cases) * 100 if total_cases > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("総テストケース数", f"{total_cases}件")
    col2.metric("合格（✅）", f"{pass_cases}件")
    col3.metric("正解率", f"{pass_rate}%")

def display_test_details(df):
    """詳細結果のテーブルを表示する"""
    st.subheader("📋 テストケース詳細")
    # 備考欄のNoneを空文字に置き換える（表示を綺麗にするため）
    df["備考"] = df["備考"].fillna("")

    st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    st.title(" 🧪精度評価・テスト結果")
    st.markdown("""本アプリケーションの回答制度を検証した結果です。""")

    CSV_PATH = os.path.join("data", "test_cases.csv")
    df = load_test_data(CSV_PATH)

    if df is not None:
        display_summary_metrics(df)
        display_test_details(df)
    else:
        st.error(f"⚠️ テストデータが見つかりません: {CSV_PATH}")
        st.info("Excel等で作成したテスト結果をCSV形式で保存し、dataフォルダに配置してください。")

if __name__ == "__main__":
    main()
