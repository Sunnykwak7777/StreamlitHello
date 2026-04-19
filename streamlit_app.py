import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import time, datetime

st.set_page_config(layout = "wide")
st.title("Streamlit 앱 레이아웃 구성하기")
with st.expander('이 앱에 대하여'):
    st.write('이 앱은 streamlit앱을 다양한 방법을 보여줍니다.')
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=100)



st.sidebar.header('입력')
user_name = st.sidebar.text_input('당신의 이름으 무엇인가요?')
user_emoji=st.sidebar.selectbox('이모티콘 선택', ['😲', '🥱', '😴', '🤤', '😪'])
user_food = st.sidebar.selectbox('가장 좋아하는 음식은?', ['','Tom yung kung', 'Burrito', 'Lasagna'])

st.header('출력')
col1, col2, col3 = st.columns(3)
with col1:
    if user_name  !='':
        st.write(f'👋 안녕하세요 {user_name}님!')
    else:
        st.write('👈 **이름**을 입력해 주세요!')

with col2:
    if user_emoji != '':
        st.write(f'{user_emoji}는 당신이 좋아하는 **이모티콘**입니다!')
    else:
        st.write('👈 **이모티콘**을 선택 해 주세요!')
with col3:
    if user_emoji != '':
        st.write(f'🍴 **{user_food}**은 당신이 좋아하는 **음식**입니다!')
    else:
        st.write('👈 가장 좋아하는 **음식**을 선택 해 주세요!')
        


st.title('st.secrets')
st.write(st.secrets.get('message', '설정된 메시지가 없습니다.'))

st.title('st.file_uploader')
st.subheader('CSV 입력')
uploaded_file = st.file_uploader("파일선택")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('DataFrame')
    st.write(df)
    st.subheader('기술 통계')
    st.write(df.describe())
else:
    st.info('CSV파일을 업로드하세요')

