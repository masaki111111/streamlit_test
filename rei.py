import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Streamlitアプリ
st.title("皮膚温度の10行前平均と10分前平均の比較")

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # CSVファイルを読み込む
    df = pd.read_csv(uploaded_file)

    # データの確認
    st.write("アップロードしたデータ:")
    st.dataframe(df.head())

    # 日時情報のカラムをdatetime型に変換
    try:
        df['datetime'] = pd.to_datetime(df.iloc[:, 1], format='%d.%m.%Y %H:%M:%S')
    except Exception as e:
        st.error("日時情報の変換に失敗しました。形式を確認してください。")
        st.stop()

    # 現在の時刻を取得
    current_time = datetime.now()

    # 現在の時刻から10分前の時刻を計算
    ten_minutes_ago = current_time - timedelta(minutes=10)

    # 現在の時刻に最も近い行を特定
    df = df.sort_values('datetime')  # 日時順にソート
    closest_row_index = (df['datetime'] - current_time).abs().idxmin()

    # 現在の時刻の行と10分前の行を抽出
    current_row = df.iloc[closest_row_index]
    ten_minutes_ago_row = df[df['datetime'] <= ten_minutes_ago].iloc[-1]

    # 現在の行から10行前の範囲
    if closest_row_index >= 10:
        current_avg = df.iloc[closest_row_index - 10:closest_row_index, 5].mean()
    else:
        st.warning("現在の時刻から10行前のデータが不足しています。")
        st.stop()

    # 10分前の行からさらに10行前の範囲
    ten_minutes_ago_index = ten_minutes_ago_row.name
    if ten_minutes_ago_index >= 10:
        past_avg = df.iloc[ten_minutes_ago_index - 10:ten_minutes_ago_index, 5].mean()
    else:
        st.warning("10分前の時刻から10行前のデータが不足しています。")
        st.stop()

    # 平均値の表示
    st.write(f"現在の時刻から10行前の平均: {current_avg:.2f}")
    st.write(f"10分前の時刻から10行前の平均: {past_avg:.2f}")

    # 差を比較
    if current_avg > past_avg:
        st.success("現在の平均は10分前の平均よりも上昇しています。")
    else:
        st.info("現在の平均は10分前の平均よりも上昇していません。")

