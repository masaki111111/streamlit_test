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
#st.write(response.text) #データを表示



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
#st.write(a1)#これでJsonデータが整列される


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
#st.write(a0)#これでJsonデータが整列される

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
#csv_file_path = "data/05_12_2024_DA38DDB3C43F_history.csv"
csv_file_path = "data/11_06_15_2024_DA38DDB3C43F_history.csv"


try:
    df = pd.read_csv(csv_file_path, sep = ';', header = 1,)
    #st.write("CSVファイルの読み込みに成功しました。")
except Exception as e:
    #st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    st.stop()

data = pd.to_datetime(df.iloc[:,1], format = '%d.%m.%Y %H:%M:%S')

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
    #st.write("CSVファイルの読み込みに成功しました。")
except Exception as e:
    #st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
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

# COREの30分前との変化率取得
chang_rate = plot_data['Temp'].pct_change(30, axis=0)
plot_data['diff30m'] = chang_rate
plot_data['diff30m'][plot_data['diff30m']==np.NaN] = 0
df_cr = pd.DataFrame(chang_rate)
df_cr['date_time_local'] = data

ss1 = '今回の睡眠スコアは'
ss2 = b
ss3 = 'でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))




# 小数点切り捨て
n = 1
m = duration_in_hrs / 3600 #total_sleep_durationは秒数で表しているので,3600で割れば時間が出る
new_duration_in_hrs = math.floor(m * 10 ** n) / (10 ** n)

ss1 = '今日の睡眠時間は'
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

#---------------------------
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
            if past_core_avg1 > current_core_avg:
                st.write("入眠に適しているといえる状態です")
        if past_skin_avg1 > current_skin_avg:
            st.write("皮膚温度が上がっていません")
                
            
            #st.write(f"1時間前と現在の皮膚温の差: {skinsub:.2f}")       
            #st.write(f"1時間前と現在の皮膚温の差: {coresub:.2f}")
                     
            


            st.caption("皮膚温が上がって深部体温が下がっている場合眠るのに良いタイミングです")
            st.caption("眠り始めの90分で、いかに深く、質の良い睡眠がとれるかで睡眠全体の質が変わります睡眠に影響を及ぼす体の温度には2種類あり、体の内部を指す「深部体温」は、睡眠中に下がり臓器や筋肉、脳などを休ませます。")
            st.caption("もう1つは「皮膚温度」です。目が覚めている時は通常、深部体温のほうが皮膚温度よりも2℃ほど高いです。そして、入眠前には皮膚温度が上昇し、手足がポカポカすることで放熱を行い、深部体温を下げ、皮膚温度と深部体温の差が2℃以下に縮まることで、黄金の90分が生まれます。")
            # 皮膚温度が下がり始めたタイミングを検出
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
        st.error("CSVファイルに少なくとも6列のデータが必要です。")
#---------------------------

