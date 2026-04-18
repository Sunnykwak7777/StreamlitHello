#import sys
#!{sys.executable} -m pip install ydata-profiling
import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import time, datetime
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
 
st.header('st.button')
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

st.header('st.write')
st.write('Hello, *World!* :sunglasses:')
st.write(1234)

df = pd.DataFrame({'첫 번째 컬럼':[1,2,3,4], '두 번째 컬럼':[10,20,30,40]})
st.write(df)

st.write('아래는 DataFrame입니다', df, '위는 dataframe입니다')

df2 = pd.DataFrame(
    np.random.randn(200,3),
    columns = ['a', 'b', 'c'])
c = alt.Chart(df2).mark_circle().encode(
    x='a', y='b', size='c', color = 'c', tooltip=['a','b', 'c'])

st.write(c)

st.header('st.slider')
st.subheader('Slider')
age = st.slider('당신의 나이는?', 0, 130, 25)
st.write("나는  ", age, '살입니다.')

st.subheader('범위슬라이더')
values = st.slider(
    '값의 범위를 선택하세요',
    0.0, 100.0, (25.0, 75.0))
st.write('값:', values)

st.subheader('시간범위 슬라이더')
appointment = st.slider(
    "약속을 예약하세요:",
    value = (time(11,30), time(12,45)))
st.write("예약된 시간:", appointment)

st.subheader('날짜 및 시간 슬라이더')
start_time = st.slider(
    "언제 시작하시겠습니까?",
    value = datetime(2020, 1,1,9,30),
    format = "MM/DD/YY - hh:mm")
st.write("시작시간:", start_time)

#st.line_chart 사용법 --> altair_chart의 간단버전이고, 우리는 plotly를 쓰는게 좋다.
st.header('라인차트')
chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns = ['a','b', 'c']
)
st.line_chart(chart_data)

#st.selectbox -->drop down 박스 만들기
st.header('st.selectbox')
option = st.selectbox(
    '가장 좋아하는 색상은 무엇인가요?',
    ('파랑', '빨강', '초록')
)

st.write('당신이 좋아하는 색상은', option)

#st.multiselect -->drop down 박스 만들기
st.header('st.multiselect')
options = st.multiselect(
    '가장 좋아하는 색상은 무엇인가요?',
    ['초록', '노랑', '빨강', '파랑'],
    ['노랑', '빨강'])   #기본값
st.write('당신이 선택한 색상:', options)

#st.checkbox
st.header('st.checkbox')
st.write('주문하고 싶은 것이 무엇인가요?')
icecream = st.checkbox('아이스크림')
coffee = st.checkbox('커피')
cola = st.checkbox('콜라')

if icecream :
    st.write("좋아요! 여기 더 많은 icecream")
if coffee :
    st.write("좋아요! 여기 더 많은 coffee") 
if cola :
    st.write("좋아요! 여기 더 많은 cola") 

#streamlit_pandas_profiling은 Python 3.14 미지원으로 비활성화
st.header('streamlit_pandas_profiling')
df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')
pr = ProfileReport(df)
html(pr.to_html(), height=600, scrolling=True)
