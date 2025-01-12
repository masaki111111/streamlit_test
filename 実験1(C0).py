import pandas as pd
import streamlit as st

df = pd.read_csv(".streamlit/果物.xlsx")
st.dataframe(data=df)
