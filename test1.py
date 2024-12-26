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

# 日本のタイムゾーンを設定
japan_tz = pytz.timezone('Asia/Tokyo')

# 現在の日本時間を取得
now = datetime.datetime.now(japan_tz)
dt_now = now.strftime('%Y-%m-%d')

# 昨日の日付を取得
yd = now - datetime.timedelta(days=1)
dt_yd = yd.strftime('%Y-%m-%d')

# 一昨日の日付を取得
dby = now - datetime.timedelta(days=2)
dt_dby = dby.strftime('%Y-%m-%d')

# 三日前の日付を取得
days_ago_3 = now - datetime.timedelta(days=3)
dt_days_ago_3 = days_ago_3.strftime('%Y-%m-%d')

# 結果を表示
print(f"今日の日付 (日本時間): {dt_now}")
print(f"昨日の日付 (日本時間): {dt_yd}")
print(f"一昨日の日付 (日本時間): {dt_dby}")
print(f"三日前の日付 (日本時間): {dt_days_ago_3}")

#期間を指定
start_text = dt_dby
end_text = dt_now

url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 
params={ 
    'start_date': '2024-06-28',#start_text,#'2024-06-28', 
    'end_date': '2024-06-30'#end_text #'2024-06-30'
}
headers = { 
  'Authorization': 'Bearer  XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.get(url, headers=headers, params=params) 
st.write(response.text) #データを表示



a2 = response.json()
#st.write(a2)#これでJsonデータが整列される


#1つの睡眠についてのドキュメント
import requests 
url = 'https://api.ouraring.com/v2/usercollection/daily_sleep'
params={ 
    'start_date': '2024-06-28', 
    'end_date': '2024-06-30'
}
headers = { 
  'Authorization': 'Bearer XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.request('GET', url, headers=headers, params=params) 
a1 =response.json()
st.write(a1)#これでJsonデータが整列される


#シングルスリープドキュメント(就寝と起床の時間を取得)
url = 'https://api.ouraring.com/v2/usercollection/sleep'
params = {
    'start_date': '2024-06-28',#start_text, #'2024-06-28', #start_text (全期間が欲しい場合)
    'end_date': '2024-06-30'#end_text #'2024-06-30' #end_text　(全期間が欲しい場合)
}
headers = { 
  'Authorization': 'Bearer XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.get(url, headers=headers, params=params) 
#st.write(response)#jsonデータ取得
a0 = response.json()
st.write(a0)#これでJsonデータが整列される

#変数に就寝と起床の時間を代入
date1 = (a0["data"][0]["bedtime_start"])
date2 = (a0["data"][0]["bedtime_end"])

date3 = (a0["data"][1]["bedtime_start"])
date4 = (a0["data"][1]["bedtime_end"])

date5 = (a0["data"][1]["bedtime_start"])#本来2
date6 = (a0["data"][1]["bedtime_end"]) #本来2

#フォーマット変更
date_start0 =pd.to_datetime(date1, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start0 = date_start0.tz_localize(None)

date_end0 =pd.to_datetime(date2, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end0 = date_end0.tz_localize(None)

date_start1 =pd.to_datetime(date3, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start1 = date_start1.tz_localize(None)

date_end1 =pd.to_datetime(date4, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end1 = date_end1.tz_localize(None)

date_start2 =pd.to_datetime(date5, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start2 = date_start2.tz_localize(None)

date_end2 =pd.to_datetime(date6, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end2 = date_end2.tz_localize(None) 


b = (a2["data"][0]["score"])#変数に一日目のスコアを代入

duration_in_hrs = (a0["data"][0]["total_sleep_duration"])#変数に一日目の睡眠時間を代入

#x_choice = st.radio("", ("今日", "昨日","一昨日"), horizontal=True, args=[1, 0])<3日間のグラフ表示変更>


#----COREのデータ取得----
#df = pd.read_csv('data/CORE_data.csv', sep = ';', header = 1,)
# CSVファイルのパスを指定
#csv_file_path = r"C:\Users\owner\OneDrive - 大阪工業大学\ウエルネス研究室\福田勝基\Core\22_08_2024_DA38DDB3C43F_history.csv"
#csv_file_path = r"g: " + os.path.join("\マイドライブ\Test1", "file.csv"
# = r"C:\CORE\介入06-12_2024_DA38DDB3C43F_history.csv"
csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"


try:
    df = pd.read_csv(csv_file_path, sep = ';', header = 1,)
    st.write("CSVファイルの読み込みに成功しました。")
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.stop()

data = pd.to_datetime(df.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')

y = df.iloc[:,2]
plot_data = pd.DataFrame(data)
plot_data['Temp'] = y

st.write("取得したデータ")
st.write(plot_data)
st.write(plot_data['Temp'])

st.write("データフレームの列名:")
st.write(df.columns)

# COREの前日データ取得
#df_yd = pd.read_csv('data/CORE_data_yd.csv', sep = ';', header = 1,)
try:
    df_yd = pd.read_csv(csv_file_path, sep = ';', header = 1,)
    st.write("CSVファイルの読み込みに成功しました。")
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
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
    st.write("CSVファイルの読み込みに成功しました。")
except Exception as e:
    st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
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
x_choice = st.radio("日付を選んでください", ("今日", "昨日", "一昨日"), horizontal=True)

if x_choice == "今日":
        fig.add_traces((f1))
if x_choice == "昨日":
        fig.add_traces((f1,f2))
if x_choice == "一昨日":
        fig.add_traces((f1,f2,f3))

if x_choice == "今日":
     
      
      

      #変数に今日のスコアを代入
      b = (a2["data"][0]["score"])
      #レム睡眠の長さ
      rem_sleep_duration = (a0["data"][0]["rem_sleep_duration"])

      #今日の睡眠時間
      duration_in_hrs = (a0["data"][0]["total_sleep_duration"])#変数に一日目の睡眠時間を代入

      # データトレースを追加
      fig.add_trace(go.Scatter(
       x=[date_start0, date_start0],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Red", width=3)
      ))
      fig.add_trace(go.Scatter(
       x=[date_end0, date_end0],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Red", width=3)
      ))                                                                                                  
      st.plotly_chart(fig,use_container_width=True) 


if x_choice == "昨日":
      fig = go.Figure()
      fig.add_traces((f1,f2))
      f2 = go.Scatter(x=plot_data['date_time_local'],#new_datetime_yd
                         y=plot_data_yd['Temp'],
                         mode='lines',
                         name='昨日の深部体温'
                        )


      #変数に昨日のスコアを代入
      b = (a2["data"][1]["score"])
      #レム睡眠の長さ
      rem_sleep_duration = (a0["data"][1]["rem_sleep_duration"])

      #昨日の睡眠時間
      duration_in_hrs = (a0["data"][1]["total_sleep_duration"])#変数に2日目の睡眠時間を代入

       # データトレースを追加
      fig.add_trace(go.Scatter(
       x=[date_start1, date_start1],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Blue", width=3)
      ))
      fig.add_trace(go.Scatter(
       x=[date_end1, date_end1],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Blue", width=3)
      ))                                            
      st.plotly_chart(fig,use_container_width=True) 

if x_choice == "一昨日":
      fig = go.Figure()
      fig.add_traces((f1,f2,f3))
      f3 = go.Scatter(x=plot_data['date_time_local'],#new_datetime_dby
                         y=plot_data_dby['Temp'],
                         mode='lines',
                         name='一昨日のの深部体温'
                        )

      #変数に一昨日のスコアを代入
      b = (a2["data"][2]["score"])
      #レム睡眠の長さ
      rem_sleep_duration = (a0["data"][2]["rem_sleep_duration"])

      #一昨日の睡眠時間
      duration_in_hrs = (a0["data"][2]["total_sleep_duration"])#変数に3日目の睡眠時間を代入

      # データトレースを追加
      fig.add_trace(go.Scatter(
       x=[date_start2, date_start2],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Green", width=3)
      ))
      fig.add_trace(go.Scatter(
       x=[date_end2, date_end2],
       y=[36, 40],
       mode='lines+markers',
       name='lines+markers',
       line=dict(color="Green", width=3)
      ))
      st.subheader('今日の概日リズム')                                                
      st.plotly_chart(fig,use_container_width=True) 

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

ss1 = '睡眠スコアは'
ss2 = b
ss3 = 'でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))


# 睡眠時間


# 小数点切り捨て
n = 1
m = duration_in_hrs / 3600 #total_sleep_durationは秒数で表しているので,3600で割れば時間が出る
new_duration_in_hrs = math.floor(m * 10 ** n) / (10 ** n)

ss1 = '睡眠時間は'
ss2 = new_duration_in_hrs
ss3 = '時間でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))


#レム睡眠
# 小数点切り捨て
n = 1
m = rem_sleep_duration / 3600 #total_sleep_durationは秒数で表しているので,3600で割れば時間が出る
#new_rem_sleep_duration = math.floor(m * 10 ** n) / (10 ** n)
new_rem_sleep_duration = round(m,2)


sss1 = 'レム睡眠は'
sss2 = new_rem_sleep_duration
sss3 = '時間でした'
st.markdown("{0}{1}{2}".format(sss1,sss2,sss3))

#レム睡眠の割合
new1_rem_sleep_duration = (new_rem_sleep_duration * 0.6) * 100

min_duration_in_hrs = new_duration_in_hrs * 60

rem_ratio = (new1_rem_sleep_duration / min_duration_in_hrs) * 100

# 小数点切り捨て
new_rem_ratio = math.floor(rem_ratio * 10 ** n) / (10 ** n) 
s1 = 'レム睡眠の割合は'
s2 = new_rem_ratio
s3 = '％です'
st.markdown("{0}{1}{2}".format(s1,s2,s3))

st.write("レム睡眠は夢を見る事、記憶の統合、学習、創造性と関連しています")
st.write("レム睡眠の量は睡眠時間全体の5~50%を占めています.成人の平均的なレム睡眠は1.5時間ですが、年齢とともに減少するのが一般的です")
st.write()
# 起床時刻と体温上がり初めの差異
