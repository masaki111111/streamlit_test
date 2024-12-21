import streamlit as st
import pandas as pd

# Googleドライブの共有リンクのFILE_IDを指定
FILE_ID = "https://docs.google.com/spreadsheets/d/1ODF3G1iM_e4IxAkhGdi6OQrQUGrA2uyl2h4wPhX-aQ8/edit?usp=drive_link"

# Googleドライブのダウンロードリンク
DOWNLOAD_URL = f"https://drive.google.com/uc?id={FILE_ID}"

# StreamlitアプリのUI
st.title("GoogleドライブのCSV表示")

st.write("以下のCSVファイルを表示しています：")
st.write(DOWNLOAD_URL)

# CSVをデータフレームとして読み込む
try:
    df = pd.read_csv(FILE_ID)
    st.dataframe(df)  # Streamlitのデータフレーム表示
except Exception as e:
    st.error(f"CSVファイルの読み込みに失敗しました: {e}")