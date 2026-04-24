import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import time

csv_url = "https://raw.githubusercontent.com/Sunnykwak7777/StreamlitHello/main/my__data.csv"
st.title('st.cache_data')

# 캐시 사용
st.subheader('st.cache_data 사용')

@st.cache_data()
def load_data_a(url):
    # pandas를 이용해 csv 파일을 읽어옵니다.
    df = pd.read_csv(url, encoding='UTF-8')
    return df

a0 = time.time()
st.write(load_data_a(csv_url))
a1 = time.time()
st.info(a1-a0)

df = load_data_a(csv_url)
st.dataframe(df)
st.write(df)

# 캐시 미사용
st.subheader('st.cache 미사용')

def load_data_b(url):
    # pandas를 이용해 csv 파일을 읽어옵니다.
    df = pd.read_csv(url, encoding='UTF-8')
    return df

b0 = time.time()
st.write(load_data_b(csv_url))
b1 = time.time()
st.info(b1-b0)