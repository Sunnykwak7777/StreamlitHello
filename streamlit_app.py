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
def slow_function(x):
  time.sleep(3)  #시간이 오래 걸리는 작업
  return x*10


a0 = time.time()
st.write(load_data_a())
a1 = time.time()
st.info(a1-a0)
result = slow_function(5)
st.write("결과:", result)

# 캐시 미사용
st.subheader('st.cache 미사용')

def load_data_b():
  df = pd.DataFrame(
    np.random.rand(2000000, 5),
    columns=['a', 'b', 'c', 'd', 'e']
  )
  return df
b0 = time.time()
st.write(load_data_b())
b1 = time.time()
st.info(b1-b0)
