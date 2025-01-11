import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Streamlitアプリ
st.title("日時を指定して平均の差を比較するプログラム")



if uploaded_file is not None:
    # CSVファイルを読み込む
    df = "data/05_12_2024_DA38DDB3C43F_history.csv"


    # データの確認
    st.write("アップロードしたデータ:")
    st.dataframe(df.head())

    # 日時情報のカラムをdatetime型に変換
    try:
        df['datetime'] = pd.to_datetime(df.iloc[:, 1], format='%d.%m.%Y %H:%M:%S')
    except Exception as e:
        st.error("日時情報の変換に失敗しました。形式を確認してください。")
        st.stop()

    # 使用者に基準となる日時を入力してもらう
    user_input_time = st.text_input("基準となる日時を入力してください（例: 05.12.2024 22:30:00）")

    if user_input_time:
        try:
            # 入力された日時をdatetime型に変換
            input_time = datetime.strptime(user_input_time, '%d.%m.%Y %H:%M:%S')

            # データを日時順にソート
            df = df.sort_values('datetime')

            # 入力された日時に最も近い行を特定
            closest_row_index = (df['datetime'] - input_time).abs().idxmin()

            # 基準時刻の行から10行前の範囲
            if closest_row_index >= 10:
                input_avg = df.iloc[closest_row_index - 10:closest_row_index, 5].mean()
            else:
                st.warning("基準時刻から10行前のデータが不足しています。")
                st.stop()

            # 基準時刻の10分前の行を特定
            ten_minutes_ago = input_time - timedelta(minutes=10)
            ten_minutes_ago_row = df[df['datetime'] <= ten_minutes_ago].iloc[-1]

            # 10分前の行からさらに10行前の範囲
            ten_minutes_ago_index = ten_minutes_ago_row.name
            if ten_minutes_ago_index >= 10:
                past_avg = df.iloc[ten_minutes_ago_index - 10:ten_minutes_ago_index, 5].mean()
            else:
                st.warning("10分前の時刻から10行前のデータが不足しています。")
                st.stop()

            # 平均値の表示
            st.write(f"基準時刻から10行前の平均: {input_avg:.2f}")
            st.write(f"10分前の時刻から10行前の平均: {past_avg:.2f}")

            # 差を比較
            if input_avg > past_avg:
                st.success("基準時刻の平均は10分前の平均よりも上昇しています。")
            else:
                st.info("基準時刻の平均は10分前の平均よりも上昇していません。")

        except Exception as e:
            st.error("日時の入力形式が正しくありません。例: 05.12.2024 22:30:00")
