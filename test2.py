import pandas as pd
import streamlit as st

# Google DriveからCSVを読み込む
url = "https://drive.google.com/open?id=1LKYgrd_3PTHcmz9avF7ArFXMD0p8SThR"
df = pd.read_csv(url, on_bad_lines='skip')


st.write(df)