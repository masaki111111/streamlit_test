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

#csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"
#csv_file_path = "data/11_06_15_2024_DA38DDB3C43F_history.csv"
csv_file_path = "data/14_01_2025_DA38DDB3C43F_history (2).csv"


#csv_file_path =""

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
# 6時以降のデータをフィルタリング（6時～9時の範囲）この数字はユーザによって変更する

df_after_6 = df[(df['datetime'].dt.hour >= 6) | (df['datetime'].dt.hour < 12)]

if df_after_6.empty:
    st.warning("6時以降のデータが見つかりません。")
else:
    # データの確認
    st.write("6時以降のデータが表示されます:")
    #st.dataframe(df_after_6)

    # 6列目（皮膚温度）と3列目（深部体温）のデータを取得
    if len(df_after_6.columns) >= 6:
        skin_temp_6 = df_after_6.iloc[:, 5]  # 6列目（皮膚温度）
        core_temp_6 = df_after_6.iloc[:, 2]  # 3列目（深部体温）

        # データが十分にあるか確認
        if len(skin_temp_6) >= 16 and len(core_temp_6) >= 16:
            # 過去10行と現在6行の平均を計算（皮膚温度）
            past_skin_av1 = skin_temp_6.iloc[-70:-60].mean() #一時間前
            past_skin_av2 = skin_temp_6.iloc[-40:-30].mean() #三十分前
            past_skin_av3 = skin_temp_6.iloc[-20:-10].mean() #十分前
            current_skin_av = skin_temp_6.iloc[-10:].mean() #現時点

            # 過去10行と現在6行の平均を計算（深部体温）
            past_core_av1 = core_temp_6.iloc[-70:-60].mean() #1時間前
            past_core_av2 = core_temp_6.iloc[-50:-40].mean() #40分前
            past_core_av3 = core_temp_6.iloc[-40:-30].mean() #30分前
            past_core_av4 = core_temp_6.iloc[-20:-10].mean() #10分前
            past_core_av5 = core_temp_6.iloc[-15:-5].mean() #5分前
            current_core_av = core_temp_6.iloc[-10:].mean()

            skinsub = past_skin_av1 - current_skin_av

            coresub = past_core_av1 - current_core_av
            
            # 平均値を表示
            st.write(f"1時間前の平均皮膚温度: {past_skin_av1:.2f}",f"。30分前の平均皮膚温度: {past_skin_av2:.2f}",f"。現在の平均皮膚温度: {current_skin_av:.2f}")
            st.write(f"1時間前の平均深部体温: {past_core_av1:.2f}",f"。30前の平均深部体温: {past_core_av2:.2f}",f"。現在の平均深部体温: {current_core_av:.2f}")
            st.write("")
            
        #深部体温が1時間前,30分前に10分前に上がっている且つ,5分前と比べて下がっているときアラーム(下限のピーク検出)
        if past_core_av1 > past_core_av2:
            if past_core_av2 < past_core_av3:
             if past_core_av3 < past_core_av4:
              if past_core_av4 < current_core_av:
                st.write("目覚めるのに最適な時間です。目覚めはどうでしたか？")
                audio_path1 = 'data/short-8bit-05.wav' #入力する音声ファイル

                audio_placeholder = st.empty()

                file_ = open(audio_path1, "rb")
                contents = file_.read()
                file_.close()

                audio_str = "data:audio/ogg;base64,%s"%(base64.b64encode(contents).decode())
                audio_html = """
                          <audio autoplay=True>
                          <source src="%s" type="audio/ogg" autoplay=True>
                          Your browser does not support the audio element.
                          </audio>
                          """ %audio_str

                audio_placeholder.empty()
                time.sleep(0.5) #これがないと上手く再生されません
                audio_placeholder.markdown(audio_html, unsafe_allow_html=True)


        if past_core_av2 < current_core_av:
            st.write("深部体温が上昇しています二度寝をせずにそのまま起きましょう")
        else:
            st.write("目覚めはどうでしたか？")
            st.write("現在深部体温が十分に上がっていません")
             
         
        
        
                
            
            #st.write(f"1時間前と現在の皮膚温の差: {skinsub:.2f}")       
            #st.write(f"1時間前と現在の深部体温の差: {coresub:.2f}")
                     
            


            st.caption("深部体温が上がっている場合起きるのに良いタイミングです")
            st.caption("深部体温の概日リズムが睡眠とうまくマッチしていると、深部体温の下がった心身が休息状態にある時によく眠ることができます")
            st.caption("しかし、深部体温リズムが前進していると、望ましい時刻より早くから眠たくなり、早朝に目覚めてしまいます。深部体温リズムが遅れていると、望ましい時刻になっても心身が休息状態になっていないため眠れず、朝は心身が休息状態から覚めていないため起床が困難になります。")
            # 皮膚温度が下がり始めたタイミングを検出
        if len(skin_temp_6) >= 16 and len(core_temp_6) >= 16:
            # 皮膚温度と深部体温の変化を検出
            for i in range(len(skin_temp_6) - 1, 9, -1):
                # 10行の平均を更新
                past_skin_avg_6 = skin_temp_6.iloc[i-40:i-30].mean()  # 過去40行-30(30分前の10分平均)
                current_skin_avg_6 = skin_temp_6.iloc[i-10:i].mean()  # 現在10行
                past_core_avg_6 = core_temp_6.iloc[i-40:i-30].mean()  # 過去40行-30(30分前の10分平均)
                current_core_avg_6 = core_temp_6.iloc[i-10:i].mean()  # 現在10行

                # 皮膚温度が下降し深部体温が上昇しているか判定
                if current_skin_avg_6 < past_skin_avg_6 and current_core_avg_6 > past_core_avg_6:
                    # 皮膚温度がしたがり、深部体温が上がり始めたタイミングの行を表示
                    st.warning(f"深部体温が上昇している時刻: {df_after_6.iloc[i]['datetime']}")
                    break  # 最初に条件を満たしたタイミングで終了

            else:
                st.info("皮膚温度が上昇し、深部体温が下降しているタイミングは見つかりませんでした。")

            
        else:
            st.warning("22時以降のデータが16行以上必要です。")
    else:
        st.error("CSVファイルに少なくとも6列のデータが必要です。")

#下から場合によって消す
#----------------------------------Oura API--------------------------------------------

# 日本のタイムゾーンを設定
japan_tz = pytz.timezone('Asia/Tokyo')

# 現在の日本時間を取得
now = datetime.datetime.now(japan_tz)
dt_now = now.strftime('%Y-%m-%d')


# 結果を表示
print(f"今日の日付 (日本時間): {dt_now}")


#期間を指定
start_text = dt_now

url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 
params={ 
    'start_date': '2025-01-13'#start_text,#'2024-06-28', 

}
headers = { 
  'Authorization': 'Bearer  OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ' 
    #OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ
    #XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS
}
response = requests.get(url, headers=headers, params=params) 
#st.write(response.text) #データを表示



a2 = response.json()
#st.write(a2)#これでJsonデータが整列される


#1つの睡眠についてのドキュメント
import requests 
url = 'https://api.ouraring.com/v2/usercollection/daily_sleep'
params={ 
    'start_date': '2025-01-13'#2024 06 30
   
}

headers = { 
  'Authorization': 'Bearer OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ' 
    #OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ
    #XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS
}
response = requests.request('GET', url, headers=headers, params=params) 
a1 =response.json()
#st.write(a1)#これでJsonデータが整列される


#シングルスリープドキュメント(就寝と起床の時間を取得)
url = 'https://api.ouraring.com/v2/usercollection/sleep'
params = {
    'start_date': '2025-01-14'#start_text, #'2024-06-28', #start_text (全期間が欲しい場合)
    #end_text #'2024-06-30' #end_text　(全期間が欲しい場合)
}
headers = { 
  'Authorization': 'Bearer OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ' 
    #OP5RQS5UOF7KKPYYGMQC4NF6ND6CE4QQ　大きいほう
    #XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS　小さいほう
}
response = requests.get(url, headers=headers, params=params) 
#st.write(response)#jsonデータ取得
a0 = response.json()
#st.write(a0)#これでJsonデータが整列される

#変数に就寝と起床の時間を代入
#date1 = (a0["data"][0]["bedtime_start"])
#---------------------エラーが出る場合ここをコメントアウト-----------------------
#date2 = (a0["data"][0]["bedtime_end"])
#-----------------------------------------------------------------------------


#フォーマット変更
#date_start0 =pd.to_datetime(date1, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
#date_start0 = date_start0.tz_localize(None)

#date_end0 =pd.to_datetime(date2, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
#date_end0 = date_end0.tz_localize(None)




b = (a2["data"][0]["score"])#変数に一日目のスコアを代入

#duration_in_hrs = (a0["data"][0]["total_sleep_duration"])#変数に一日目の睡眠時間を代入

#x_choice = st.radio("", ("今日", "昨日","一昨日"), horizontal=True, args=[1, 0])<3日間のグラフ表示変更>


#-----------------------------------core データ----------------------------------------------------


y = df.iloc[:,2]
plot_data = pd.DataFrame(data)
plot_data['Temp'] = y

#st.write("取得したデータ")
#st.write(plot_data)
#st.write(plot_data['Temp'])

#st.write("データフレームの列名:")
#st.write(df.columns)

# COREの前日データ取得
#df_yd = pd.read_csv('data/CORE_data_yd.csv', sep = ';', header = 1,)
try:
    df_yd = pd.read_csv(csv_file_path, sep = ';', header = 1,)
 
except Exception as e:
  
    st.stop()

data_yd = pd.to_datetime(df_yd.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')

y_yd = df_yd.iloc[:,2]
plot_data_yd = pd.DataFrame(data_yd)
plot_data_yd['Temp'] = y_yd
new_datetime_yd = plot_data_yd['date_time_local'] + datetime.timedelta(days=1)


# COREの一昨日のデータ
#df_dby = pd.read_csv('data/CORE_data_dby.csv', sep = ';', header = 1)
try:
    df_dby = pd.read_csv(csv_file_path, sep = ';', header = 1,)
    
except Exception as e:
    
    st.stop()

data_dby = pd.to_datetime(df_dby.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')

y_dby = df_dby.iloc[:,2]
plot_data_dby = pd.DataFrame(data_dby)
plot_data_dby['Temp'] = y_dby
new_datetime_dby = plot_data_dby['date_time_local'] + datetime.timedelta(days=2)


# CORE,Ouraプロット
fig = go.Figure()
f1 = go.Scatter(x=plot_data['date_time_local'],
                         y=plot_data['Temp'],
                         mode='lines',
                         name='今日の深部体温',
                        )
f2 = go.Scatter(x=plot_data['date_time_local'],#new_datetime_yd
                         y=plot_data_yd['Temp'],
                         mode='lines',
                         name='昨日の深部体温'
                        )

f3 = go.Scatter(x=plot_data['date_time_local'],#new_datetime_dby
                         y=plot_data_dby['Temp'],
                         mode='lines',
                         name='一昨日のの深部体温'
                        )

# 表示グラフ選択






#----------------------------------Core,ouraプロット--------------------------------------------



fig = go.Figure()
fig.add_traces(f1)
f1 = go.Scatter(x=plot_data['date_time_local'],#new_datetime_yd
                         y=plot_data_yd['Temp'],
                         mode='lines',
                         name='今日の深部体温'
                        )
#変数に今日のスコアを代入
#b = (a2["data"][0]["score"])
#レム睡眠の長さ
#rem_sleep_duration = (a0["data"][0]["rem_sleep_duration"])

#今日の睡眠時間
#duration_in_hrs = (a0["data"][0]["total_sleep_duration"])#変数に一日目の睡眠時間を代入

# データトレースを追加
fig.add_trace(go.Scatter(
#x=[date_start0],
#y=[36, 40],
mode='lines+markers',
name='入眠時間',
line=dict(color="Red", width=3)
))
fig.add_trace(go.Scatter(
#x=[date_end0, date_end0],
#y=[36, 40],
mode='lines+markers',
name='起床時間',
line=dict(color="Red", width=3)
))                                                                                                  

st.subheader('今日の概日リズム')                                                
st.plotly_chart(fig,use_container_width=True)


#-----------------------------------------------jpeg表示----------------------------------

import streamlit as st
from PIL import Image

# JPEGファイルを読み込む
image_path = "data/深部体温例.jpg"  # JPEGファイルのパス
image = Image.open(image_path)

# 画像をStreamlitで表示
st.image(image, caption="Sample JPEG Image", use_column_width=True)

st.write("上図のように深部体温は入眠の際に下がり、起床に際して上がります。この場合よい睡眠がとれるといわれています")
