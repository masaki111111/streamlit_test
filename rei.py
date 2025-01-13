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
import streamlit as st
import streamlit.components.v1 as stc
import base64
import time






    
#-----------------------------------------------------------------
#csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"
#csv_file_path = "data/11_06_15_2024_DA38DDB3C43F_history.csv"
#csv_file_path = "data/12_01_2025_DA38DDB3C43F_history.csv"
#csv_file_path = "data/13_01_2025_DA38DDB3C43F_history.csv"
csv_file_path = "data/13_01_2025_C0462D9B6C53_history.csv"

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
    st.write("22時以降のデータが表示されます:")
    #st.dataframe(df_after_22)

    # 6列目（皮膚温度）と3列目（深部体温）のデータを取得
    if len(df_after_22.columns) >= 6:
        skin_temp = df_after_22.iloc[:, 5]  # 6列目（皮膚温度）
        core_temp = df_after_22.iloc[:, 2]  # 3列目（深部体温）

        # データが十分にあるか確認
        if len(skin_temp) >= 16 and len(core_temp) >= 16:
            # 過去10行と現在6行の平均を計算（皮膚温度）
            past_skin_avg1 = skin_temp.iloc[-70:-60].mean()
            past_skin_avg2 = skin_temp.iloc[-40:-30].mean()
            current_skin_avg = skin_temp.iloc[-10:].mean()

            # 過去10行と現在6行の平均を計算（深部体温）
            past_core_avg1 = core_temp.iloc[-70:-60].mean()
            past_core_avg2 = core_temp.iloc[-40:-30].mean()
            current_core_avg = core_temp.iloc[-10:].mean()

            skinsub = past_skin_avg1 - current_skin_avg

            coresub = past_core_avg1 - current_core_avg
            
            # 平均値を表示
            st.write(f"1時間前の平均皮膚温度: {past_skin_avg1:.2f}",f"。30分前の平均皮膚温度: {past_skin_avg2:.2f}",f"。現在の平均皮膚温度: {current_skin_avg:.2f}")
            st.write(f"1時間前の平均深部体温: {past_core_avg1:.2f}",f"。30前の平均深部体温: {past_core_avg2:.2f}",f"。現在の平均深部体温: {current_core_avg:.2f}")
            st.write("")
        if past_skin_avg1 < current_skin_avg:
            if past_core_avg1 < current_core_avg:
                st.write("皮膚温度が上がり始めていますが深部体温が下がっていません")
                st.caption("皮膚温が上がって深部体温が下がっている場合眠るのに良いタイミングです")
                st.caption("眠り始めの90分で、いかに深く、質の良い睡眠がとれるかで睡眠全体の質が変わります睡眠に影響を及ぼす体の温度には2種類あり、体の内部を指す「深部体温」は、睡眠中に下がり臓器や筋肉、脳などを休ませます。")
                st.caption("もう1つは「皮膚温度」です。目が覚めている時は通常、深部体温のほうが皮膚温度よりも2℃ほど高いです。そして、入眠前には皮膚温度が上昇し、手足がポカポカすることで放熱を行い、深部体温を下げ、皮膚温度と深部体温の差が2℃以下に縮まることで、黄金の90分が生まれます。")
            # 皮膚温度が下がり始めたタイミングを検出
            if past_core_avg1 > current_core_avg:
                st.write("入眠に適しているといえる状態です")
                st.caption("皮膚温が上がって深部体温が下がっている場合眠るのに良いタイミングです")
                st.caption("眠り始めの90分で、いかに深く、質の良い睡眠がとれるかで睡眠全体の質が変わります睡眠に影響を及ぼす体の温度には2種類あり、体の内部を指す「深部体温」は、睡眠中に下がり臓器や筋肉、脳などを休ませます。")
                st.caption("もう1つは「皮膚温度」です。目が覚めている時は通常、深部体温のほうが皮膚温度よりも2℃ほど高いです。そして、入眠前には皮膚温度が上昇し、手足がポカポカすることで放熱を行い、深部体温を下げ、皮膚温度と深部体温の差が2℃以下に縮まることで、黄金の90分が生まれます。")
            # 皮膚温度が下がり始めたタイミングを検出

        if past_skin_avg1 > current_skin_avg:
            st.write("皮膚温度が上がっていません")
            st.caption("皮膚温が上がって深部体温が下がっている場合眠るのに良いタイミングです")
            st.caption("眠り始めの90分で、いかに深く、質の良い睡眠がとれるかで睡眠全体の質が変わります睡眠に影響を及ぼす体の温度には2種類あり、体の内部を指す「深部体温」は、睡眠中に下がり臓器や筋肉、脳などを休ませます。")
            st.caption("もう1つは「皮膚温度」です。目が覚めている時は通常、深部体温のほうが皮膚温度よりも2℃ほど高いです。そして、入眠前には皮膚温度が上昇し、手足がポカポカすることで放熱を行い、深部体温を下げ、皮膚温度と深部体温の差が2℃以下に縮まることで、黄金の90分が生まれます。")
            # 皮膚温度が下がり始めたタイミングを検出
            
           
            #st.write(f"1時間前と現在の皮膚温の差: {skinsub:.2f}")       
            #st.write(f"1時間前と現在の皮膚温の差: {coresub:.2f}")
                     
            



        if len(skin_temp) >= 16 and len(core_temp) >= 16:
            # 皮膚温度と深部体温の変化を検出
            for i in range(len(skin_temp) - 1, 9, -1):
                # 10行の平均を更新
                past_skin_avg = skin_temp.iloc[i-70:i-60].mean()  # 過去70行-60(一時間前の10分平均)
                current_skin_avg = skin_temp.iloc[i-10:i].mean()  # 現在10行
                past_core_avg = core_temp.iloc[i-70:i-60].mean()  # 過去70行-60(一時間前の10分平均)
                current_core_avg = core_temp.iloc[i-10:i].mean()  # 現在10行

                # 皮膚温度が上昇し、深部体温が下降しているか判定
                if current_skin_avg > past_skin_avg and current_core_avg < past_core_avg:
                    # 皮膚温度が上がり、深部体温が下がり始めたタイミングの行を表示
                    st.warning(f"皮膚温度が上昇し、深部体温が下降している時刻: {df_after_22.iloc[i]['datetime']}")
                    break  # 最初に条件を満たしたタイミングで終了

            else:
                st.info("皮膚温度が上昇し、深部体温が下降しているタイミングは見つかりませんでした。")

            
        else:
            st.warning("22時以降のデータが16行以上必要です。")
    else:
        st.warning("22時以降のデータが16行以上必要です。")
