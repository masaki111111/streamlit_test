import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# 日時変換関数
def convert_to_datetime(df, column_name, date_format):
    try:
        df['datetime'] = pd.to_datetime(df[column_name], format=date_format)
    except Exception as e:
        st.error(f"日時情報の変換に失敗しました。エラー: {e}")
        st.stop()

# 平均値計算関数
def calculate_average(df, start_index, num_rows, column_name):
    if start_index >= num_rows:
        return df.iloc[start_index - num_rows:start_index][column_name].mean()
    else:
        return None

# メイン処理
def main():
    # ダミーデータの準備（例として読み込むデータ）
    data = {
        'timestamp': ["01.01.2025 12:00:00", "01.01.2025 12:01:00", "01.01.2025 12:02:00",
                      "01.01.2025 12:03:00", "01.01.2025 12:04:00", "01.01.2025 12:05:00",
                      "01.01.2025 12:06:00", "01.01.2025 12:07:00", "01.01.2025 12:08:00",
                      "01.01.2025 12:09:00", "01.01.2025 12:10:00"],
        'value': [10, 12, 15, 14, 13, 20, 18, 16, 17, 22, 24]
    }
    df = pd.DataFrame(data)

    # 日時変換
    convert_to_datetime(df, 'timestamp', '%d.%m.%Y %H:%M:%S')

    # 現在の時刻と10分前の時刻
    current_time = datetime.now()
    ten_minutes_ago = current_time - timedelta(minutes=10)

    # 現在の時刻に最も近い行を特定
    df = df.sort_values('datetime')
    closest_index = (df['datetime'] - current_time).abs().idxmin()

    # 10分前の時刻に最も近い行を特定
    ten_minutes_index = df[df['datetime'] <= ten_minutes_ago].index[-1] if not df[df['datetime'] <= ten_minutes_ago].empty else None

    # 現在の平均値計算
    current_avg = calculate_average(df, closest_index, 10, 'value')
    if current_avg is None:
        st.warning("現在の時刻から10行前のデータが不足しています。")
        st.stop()

    # 10分前の平均値計算
    if ten_minutes_index is not None:
        past_avg = calculate_average(df, ten_minutes_index, 10, 'value')
        if past_avg is None:
            st.warning("10分前の時刻から10行前のデータが不足しています。")
            st.stop()
    else:
        st.warning("10分前の時刻に該当するデータがありません。")
        st.stop()

    # 結果表示
    st.write(f"現在の時刻から10行前の平均値: {current_avg:.2f}")
    st.write(f"10分前の時刻から10行前の平均値: {past_avg:.2f}")

    # 平均値の比較
    if current_avg > past_avg:
        st.success("現在の平均は10分前の平均よりも上昇しています。")
    else:
        st.info("現在の平均は10分前の平均よりも上昇していません。")

# 実行
if __name__ == "__main__":
    main()
