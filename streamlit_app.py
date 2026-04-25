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
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        st.success("처리가 모두 끝났습니다.")   
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
    return joblib.load(os.path.join(BASE_DIR, "model.pkl"))

model = load_model()
prediction = model.predict([[1, 2, 3]])
st.write("예측값:", prediction)

# DB 연결 캐싱
st.subheader("DB 조회 (st.cache_resource)")

@st.cache_resource
def get_connection():
    return sqlite3.connect(os.path.join(BASE_DIR, "my_database.db"), check_same_thread=False)

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

# st.spinner()

st.header("데이터 처리 진행 상황")
st.write("데이터를 불러옵니다...")
with st.spinner("잠시만 기다려 주세요...") :
    time.sleep(5)
st.success("데이타로딩 완료!")

with st.spinner("전체 작업 진행중..."):
    progress = st.progress(0)
    status_text = st.empty()  #텍스트 덮어쓰기 용 공간확보
    for i in range(5):
        status_text.write(f"       Step {i+1}/5 : 데이터 준비중...   ")
        time.sleep(1)
        progress.progress((i+1)*20)
st.success("처리가 모두 끝났습니다")
        
# st.session_state()
st.title("⚽ Boared API앱")
st.sidebar.header('입력')
selected_type = st.sidebar.selectbox('활동 유형 선택', ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])
#https://bored-api.appbrewery.com/
suggested_activity_url = f"https://bored-api.appbrewery.com/api/activity?type={selected_type}"

try:
    json_data = requests.get(suggested_activity_url, timeout=5)
    json_data.raise_for_status()
    suggested_activity = json_data.json()

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("이 앱에 대하여"):
            st.write("지루하신가요? **Boared API앱**은 지루할 때 할 수 있는 일는 활동을 제안합니다. 이 앱은 Boared API에 의해 구동됩니다.")
    with c2:
        with st.expander("JSON 데이터"):
            st.write(suggested_activity)
    st.header("제안된 활동")
    st.info(suggested_activity['activity'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label='참가자 수', value=suggested_activity['participants'], delta='')
    with col2:
        st.metric(label='활동유형', value=suggested_activity['type'].capitalize(), delta='')
    with col3:
        st.metric(label='가격', value=suggested_activity['price'], delta='')

except requests.exceptions.ConnectionError:
    st.error("Bored API 서버에 연결할 수 없습니다. 서버가 종료되었거나 네트워크를 확인해주세요.")
except requests.exceptions.JSONDecodeError:
    st.error(f"API 응답을 JSON으로 파싱할 수 없습니다. (HTTP {json_data.status_code})")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")


#model.pkl은 어떻게 만들었어?
#import joblib
#import numpy as np
#from sklearn.linear_model import LinearRegression

## 학습 데이터 (특성 3개)
#X = np.array([[1,2,3],[4,5,6],[7,8,9],[2,3,4],[5,6,7]])
#y = np.array([10, 25, 40, 15, 30])

## 선형회귀 모델 학습
#model = LinearRegression()
#model.fit(X, y)

## 파일로 저장
#joblib.dump(model, 'model.pkl')
#핵심 개념:

#단계	설명
#LinearRegression()	scikit-learn의 선형회귀 모델 생성
#model.fit(X, y)	X(입력 3개 특성), y(정답값)으로 학습
#joblib.dump(model, 'model.pkl')	학습된 모델을 파일로 직렬화(저장)
#joblib.load('model.pkl')	저장된 모델을 불러와서 재사용
#.pkl은 Python의 pickle 형식으로, 객체를 바이트로 직렬화한 파일입니다. joblib은 numpy 배열이 포함된 모델을 pickle보다 효율적으로 저장해주기 때문에 머신러닝에서 주로 사용됩니다.
#실제 서비스에서는 이 자리에 직접 학습한 모델(예: 집값 예측, 이미지 분류 등)의 .pkl 파일을 넣으면 됩니다.