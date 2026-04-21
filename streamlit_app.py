import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import time, datetime
import time

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

st.header('데이터 프로파일링')
df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')

st.subheader('데이터 미리보기')
st.dataframe(df)

st.subheader('기본 통계')
st.dataframe(df.describe())

st.subheader('컬럼 정보')
col_info = pd.DataFrame({
    '데이터타입': df.dtypes,
    '결측값 수': df.isnull().sum(),
    '결측값 비율(%)': (df.isnull().sum() / len(df) * 100).round(2)
})
st.dataframe(col_info)

st.subheader('수치형 컬럼 분포')
num_cols = df.select_dtypes(include='number').columns.tolist()
selected_col = st.selectbox('컬럼 선택', num_cols)
st.bar_chart(df[selected_col].value_counts().sort_index())

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

st.title('st.progress')
with st.expander('이 앱에 대하여'):
    st.write("'st.progress'명령어를 사용하여 Streamlit앱에서 계산의 진행 상태를 표시할 수 있습니다.")
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.05)
    my_bar.progress(percent_complete+1)

st.balloons()

