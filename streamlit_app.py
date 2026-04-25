import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import time
import requests
import xml.etree.ElementTree as ET
from io import BytesIO
import xlsxwriter
import joblib
import sqlite3

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

# API로 대시보드 띄우기 - 
# 1. 페이지 설정
st.set_page_config(page_title="아파트 실거래가 조회 보드", layout="wide")

# 2. API 설정 정보
API_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
SERVICE_KEY = "685c2b993815dce3876298374fbcb215a7ed176d49c6579cdb1e7bc84b534f1b"

st.title("🏙️ 국토교통부 아파트 실거래가 조회")
st.info("서울시(11110)의 2026년 3월 실거래 내역을 가져옵니다.")

# 3. 데이터 로드 함수
def fetch_apartment_data():
    # API에 보낼 파라미터 설정
    params = {
        'serviceKey': SERVICE_KEY,
        'LAWD_CD': '11110',      # 지역코드 (종로구)
        'DEAL_YMD': '202603',    # 계약년월
        'pageNo' : '1',
        'numOfRows': '200'       # 가져올 행 수
    }
    
    try:
        # API 호출
        response = requests.get(API_URL, params=params)
        
        # XML 데이터 파싱
        root = ET.fromstring(response.content)
        
        items_list = []
        # XML 구조에서 <item> 태그 안에 있는 정보들을 추출
        for item in root.findall('.//item'):
            item_dict = {
                '아파트': item.findtext('aptNm'),
                '금액(만원)': item.findtext('dealAmount'),
                '전용면적(㎡)': item.findtext('excluUseAr'),
                '층': item.findtext('floor'),
                '년': item.findtext('dealYear'),
                '월': item.findtext('dealMonth'),
                '일': item.findtext('dealDay'),
                '법정동': item.findtext('umdNm')
            }
            items_list.append(item_dict)
            
        return pd.DataFrame(items_list)
    except Exception as e:
        st.error(f"데이터를 가져오는데 실패했습니다: {e}")
        return pd.DataFrame()

# 4. 화면 출력 및 엑셀 다운로드 로직
df = fetch_apartment_data()

if not df.empty:
    # (1) 표 출력
    st.dataframe(df, use_container_width=True)
    
    # (2) 엑셀 변환 (메모리 내 작업)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # (3) 다운로드 버튼 생성
    st.download_button(
        label="📥 엑셀 파일로 다운로드",
        data=output.getvalue(),
        file_name="아파트_실거래가_202603.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("조회된 데이터가 없습니다. API 키나 파라미터를 확인해주세요.")

# 머신러닝 모델 캐싱
st.subheader("머신러닝 모델 예측 (st.cache_resource)")

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()
prediction = model.predict([[1, 2, 3]])
st.write("예측값:", prediction)

# DB 연결 캐싱
st.subheader("DB 조회 (st.cache_resource)")

@st.cache_resource
def get_connection():
    return sqlite3.connect("my_database.db", check_same_thread=False)

conn = get_connection()
df = pd.read_sql("SELECT * FROM users", conn)
st.dataframe(df)

# session_state 참고파일

st.title('st.session_state')

def lbs_to_kg():
  st.session_state.kg = st.session_state.lbs/2.2046
def kg_to_lbs():
  st.session_state.lbs = st.session_state.kg*2.2046

st.header('입력')
col1, spacer, col2 = st.columns([2,1,2])
with col1:
  pounds = st.number_input("파운드:", key = "lbs", on_change = lbs_to_kg)
with col2:
  kilogram = st.number_input("킬로그램:", key = "kg", on_change = kg_to_lbs)

st.header('출력')
st.write("st.session_state 객체:", st.session_state)