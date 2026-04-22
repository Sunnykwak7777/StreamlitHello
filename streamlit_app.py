import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import time

st.title('st.cache_data')

# 캐시 사용
st.subheader('st.cache_data 사용')

@st.cache_data()
def load_data_a():
  df = pd.DataFrame(
    np.random.rand(2000000, 5),
    columns=['a', 'b', 'c', 'd', 'e']
  )
  return df
@st.cache_data()
def slow_function_a(x):
  time.sleep(3)  #시간이 오래 걸리는 작업
  return x*10
@st.cache_data()
def load_data():
  return pd.read_csv("my_data.csv")

a0 = time.time()
st.write(load_data_a())
a1 = time.time()
st.info(a1-a0)

df = load_data()
st.dataframe(df)
st.write(df)

# 캐시 미사용
st.subheader('st.cache 미사용')

def load_data_b():
  df = pd.DataFrame(
    np.random.rand(2000000, 5),
    columns=['a', 'b', 'c', 'd', 'e']
  )
  return df

def slow_function_b(x):
  time.sleep(3)  #시간이 오래 걸리는 작업
  return x*10

b0 = time.time()
st.write(load_data_b())
b1 = time.time()
st.info(b1-b0)

result = slow_function_a(15)
st.write("결과a:", result)
result = slow_function_b(15)
st.write("결과b:", result)
