import plotly.graph_objects as go
import requests
import streamlit as st
import numpy as np
import pandas as pd
import json
import oura
import datetime
import time
import plotly.graph_objects as go
import pytz
import math
import matplotlib.pyplot as plt
import datetime
import pytz

# Streamlitアプリ
st.title("日時を指定して平均の差を比較するプログラム")



csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"

try:
    df = pd.read_csv(csv_file_path, sep = ';', header = 1,)
  
except Exception as e:

    st.stop()

data = pd.to_datetime(df.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')

# 日時情報のカラムをdatetime型に変換
try:
    df['datetime'] = pd.to_datetime(df.iloc[:, 1], format='%d.%m.%Y %H:%M:%S')
except Exception as e:
    st.error("日時情報の変換に失敗しました。形式を確認してください。")
    st.stop()

# 使用者に基準となる日時を入力してもらう
# 日時の入力 (日付と時間を分けて入力)

min_date = datetime.date(1900, 1, 1)
max_date = datetime.date(2100, 12, 31)
result = st.slider('調査期間を指定してください。', value=(min_date, max_date), format='YYYY-MM-DD (ddd)', min_value=min_date, max_value=max_date)
st.write('開始日は：', result[0])
st.write('終了日は：', result[1])

# 入力内容を表示
st.write(f"選択した時刻: {time_input}")
date_input = st.date_input("基準となる日付を選択してください")
time_input = st.time_input("基準となる時刻を選択してください")

# 入力を結合して基準日時を作成
if date_input and time_input:
    user_input_time = datetime.combine(date_input, time_input)
    st.write(f"基準日時: {user_input_time.strftime('%d.%m.%Y %H:%M:%S')}")

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
