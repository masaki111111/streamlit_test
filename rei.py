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

import streamlit as st
import pandas as pd
import datetime

csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"

try:
    df = pd.read_csv(csv_file_path, sep = ';', header = 1,)
  
except Exception as e:

    st.stop()

data = pd.to_datetime(df.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')
# CSVファイル読み込み（例）
# df = pd.read_csv('data.csv')

# 日時の変換
try:
    df['datetime'] = pd.to_datetime(df.iloc[:, 1], format='%d.%m.%Y %H:%M:%S')
except Exception as e:
    st.error("日時情報の変換に失敗しました。形式を確認してください。")
    st.stop()

# 22時以降のデータをフィルタリング（22時～翌日4時の範囲）
df_after_22 = df[(df['datetime'].dt.hour >= 22) | (df['datetime'].dt.hour < 4)]

if df_after_22.empty:
    st.warning("22時以降のデータが見つかりません。")
else:
    # データの確認
    st.write("22時以降のデータ:")
    st.dataframe(df_after_22)

    # 6列目（皮膚温度）と3列目（深部体温）のデータを取得
    if len(df_after_22.columns) >= 6:
        skin_temp = df_after_22.iloc[:, 5]  # 6列目（皮膚温度）
        core_temp = df_after_22.iloc[:, 2]  # 3列目（深部体温）

        # データが十分にあるか確認
        if len(skin_temp) >= 16 and len(core_temp) >= 16:
            # 過去10行と現在6行の平均を計算（皮膚温度）
            past_skin_avg = skin_temp.iloc[-16:-10].mean()
            current_skin_avg = skin_temp.iloc[-6:].mean()

            # 過去10行と現在6行の平均を計算（深部体温）
            past_core_avg = core_temp.iloc[-16:-10].mean()
            current_core_avg = core_temp.iloc[-6:].mean()

            # 平均値を表示
            st.write(f"過去10行（6行前まで）の平均皮膚温度: {past_skin_avg:.2f}")
            st.write(f"現在6行の平均皮膚温度: {current_skin_avg:.2f}")
            st.write(f"過去10行（6行前まで）の平均深部体温: {past_core_avg:.2f}")
            st.write(f"現在6行の平均深部体温: {current_core_avg:.2f}")

            # 皮膚温度が下がり始めたタイミングを検出
            if current_skin_avg < past_skin_avg:
                st.warning("皮膚温度が下がり始めた可能性があります。")

            # 条件を判定
            if current_skin_avg > past_skin_avg and current_core_avg < past_core_avg:
                st.success("条件を満たしました: 皮膚温度は上昇し、深部体温は下降しています。")
            else:
                st.info("条件を満たしていません。")
        else:
            st.warning("22時以降のデータが16行以上必要です。")
    else:
        st.error("CSVファイルに少なくとも6列のデータが必要です。")

