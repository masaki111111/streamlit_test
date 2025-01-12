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

csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"
#csv_file_path = "data/11_06_15_2024_DA38DDB3C43F_history.csv"

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


#-----------------------------------起床のCORE----------------------------------------------
# 6時以降のデータをフィルタリング（6時～9時の範囲）

df_after_6 = df[(df['datetime'].dt.hour >= 6) ]

if df_after_6.empty:
    st.warning("22時以降のデータが見つかりません。")
else:
    # データの確認
    st.write("6時以降のデータが表示されます:")
    st.dataframe(df_after_6)

    # 6列目（皮膚温度）と3列目（深部体温）のデータを取得
    if len(df_after_6.columns) >= 6:
        skin_temp_6 = df_after_6.iloc[:, 5]  # 6列目（皮膚温度）
        core_temp_6 = df_after_6.iloc[:, 2]  # 3列目（深部体温）

        # データが十分にあるか確認
        if len(skin_temp_6) >= 16 and len(core_temp_6) >= 16:
            # 過去10行と現在6行の平均を計算（皮膚温度）
            past_skin_av1 = skin_temp_6.iloc[-70:-60].mean()
            past_skin_av2 = skin_temp_6.iloc[-40:-30].mean()
            current_skin_av = skin_temp_6.iloc[-10:].mean()

            # 過去10行と現在6行の平均を計算（深部体温）
            past_core_av1 = core_temp_6.iloc[-70:-60].mean()
            past_core_av2 = core_temp_6.iloc[-40:-30].mean()
            current_core_av = core_temp_6.iloc[-10:].mean()

            skinsub = past_skin_av1 - current_skin_av

            coresub = past_core_av1 - current_core_av
            
            # 平均値を表示
            st.write(f"1時間前の平均皮膚温度: {past_skin_av1:.2f}",f"。30分前の平均皮膚温度: {past_skin_av2:.2f}",f"。現在の平均皮膚温度: {current_skin_av:.2f}")
            st.write(f"1時間前の平均深部体温: {past_core_av1:.2f}",f"。30前の平均深部体温: {past_core_av2:.2f}",f"。現在の平均深部体温: {current_core_av:.2f}")
            st.write("")
        if past_skin_av1 < current_skin_av:
            if past_core_av1 < current_core_av:
                st.write("皮膚温度が上がり始めていますが深部体温が下がっていません")
            if past_core_av1 > current_core_av:
                st.write("入眠に適しているといえる状態です")
        if past_skin_av1 > current_skin_av:
            st.write("皮膚温度が上がっていません")
                
            
            #st.write(f"1時間前と現在の皮膚温の差: {skinsub:.2f}")       
            #st.write(f"1時間前と現在の皮膚温の差: {coresub:.2f}")
                     
            


            st.caption("皮膚温が上がって深部体温が下がっている場合眠るのに良いタイミングです")
            st.caption("眠り始めの90分で、いかに深く、質の良い睡眠がとれるかで睡眠全体の質が変わります睡眠に影響を及ぼす体の温度には2種類あり、体の内部を指す「深部体温」は、睡眠中に下がり臓器や筋肉、脳などを休ませます。")
            st.caption("もう1つは「皮膚温度」です。目が覚めている時は通常、深部体温のほうが皮膚温度よりも2℃ほど高いです。そして、入眠前には皮膚温度が上昇し、手足がポカポカすることで放熱を行い、深部体温を下げ、皮膚温度と深部体温の差が2℃以下に縮まることで、黄金の90分が生まれます。")
            # 皮膚温度が下がり始めたタイミングを検出
        if len(skin_temp_6) >= 16 and len(core_temp_6) >= 16:
            # 皮膚温度と深部体温の変化を検出
            for i in range(len(skin_temp_6) - 1, 9, -1):
                # 10行の平均を更新
                past_skin_avg_6 = skin_temp_6.iloc[i-70:i-60].mean()  # 過去70行-60(一時間前の10分平均)
                current_skin_avg_6 = skin_temp_6.iloc[i-10:i].mean()  # 現在10行
                past_core_avg_6 = core_temp_6.iloc[i-70:i-60].mean()  # 過去70行-60(一時間前の10分平均)
                current_core_avg_6 = core_temp_6.iloc[i-10:i].mean()  # 現在10行

                # 皮膚温度下降し、深部体温が上昇しているか判定
                if current_skin_avg_6 < past_skin_avg_6 and current_core_avg_6 > past_core_avg_6:
                    # 皮膚温度が上がり、深部体温が下がり始めたタイミングの行を表示
                    st.warning(f"皮膚温度が上昇し、深部体温が下降している時刻: {df_after_6.iloc[i]['datetime']}")
                    break  # 最初に条件を満たしたタイミングで終了

            else:
                st.info("皮膚温度が上昇し、深部体温が下降しているタイミングは見つかりませんでした。")

            
        else:
            st.warning("22時以降のデータが16行以上必要です。")
    else:
        st.error("CSVファイルに少なくとも6列のデータが必要です。")
