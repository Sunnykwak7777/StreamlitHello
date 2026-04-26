import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import requests
import xml.etree.ElementTree as ET
from io import BytesIO
import xlsxwriter
import joblib
import sqlite3
import os
from datetime import time, datetime
import time as time_module


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
try:
    st.write(st.secrets.get('message', '설정된 메시지가 없습니다.'))
except Exception:
    st.write('설정된 메시지가 없습니다.')

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
    time_module.sleep(0.05)
    my_bar.progress(percent_complete+1)

st.balloons()

st.title('st.form')

# 'with' 표기법을 사용한 전체 예시
st.header('1. `with` 표기법 사용 예시')
st.subheader('커피 머신')

with st.form('my_form'):
    st.subheader('**커피 주문하기**')

    # 입력 위젯
    coffee_bean_val = st.selectbox('커피콩', ['아라비카', '로부스타'])
    coffee_roast_val = st.selectbox('커피 로스팅', ['라이트', '미디엄', '다크'])
    brewing_val = st.selectbox('추출 방법', ['에어로프레스', '드립', '프렌치 프레스', '모카 포트', '사이폰'])
    serving_type_val = st.selectbox('서빙 형식', ['핫', '아이스', '프라페'])
    milk_val = st.select_slider('우유 정도', ['없음', '낮음', '중간', '높음'])
    owncup_val = st.checkbox('자신의 컵 가져오기')

    # 모든 양식은 제출 버튼을 가져야 함
    submitted = st.form_submit_button('제출')

if submitted:
    st.markdown(f'''
        ☕ 주문하신 내용:
        - 커피콩: `{coffee_bean_val}`
        - 커피 로스팅: `{coffee_roast_val}`
        - 추출 방법: `{brewing_val}`
        - 서빙 형식: `{serving_type_val}`
        - 우유: `{milk_val}`
        - 자신의 컵 가져오기: `{owncup_val}`
        ''')
else:
    st.write('☝️ 주문하세요!')


# 객체 표기법을 사용한 짧은 예시
st.header('2. 객체 표기법 예시')

form = st.form('my_form_2')
selected_val = form.slider('값 선택')
form.form_submit_button('제출')

st.write('선택된 값: ', selected_val)

st.title('st.experimental_get_query_params')

with st.expander('이 앱에 대하여'):
  st.write("`st.experimental_get_query_params`는 사용자 브라우저의 URL에서 직접 쿼리 매개변수를 검색할 수 있게 해줍니다.")

# 1. 지침  --> query_param 사용법 유의해야함
st.header('1. 지침')
st.markdown('''
인터넷 브라우저의 URL 바에서 다음을 추가하세요:
`?firstname=Jack&surname=Beanstalk`
기본 URL `https://whitehairwitch.streamlit.app/` 뒤에 추가하여
`https://whitehairwitch.streamlit.app/?firstname=Jack&surname=Beanstalk`가 되도록 합니다.
''')
# 원인: st.experimental_get_query_params()는 Streamlit 최신 버전에서 제거된 함수입니다. 대신 st.query_params를 사용해야 합니다. 또한 새 API는 값을 리스트가 아닌 문자열로 직접 반환합니다.

# 2. st.query_params의 내용
st.header('2. st.query_params의 내용')
st.write(dict(st.query_params))


# 3. URL에서 정보 검색 및 표시
st.header('3. URL에서 정보 검색 및 표시')

firstname = st.query_params.get('firstname','')
surname = st.query_params.get('surname', '')

if firstname and surname:
    st.write(f'안녕하세요 **{firstname} {surname}**, 어떠세요?')
else:
    st.info('URL에 ?firstname=이름&surname=성 을 추가해 주세요.')

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

a0 = time_module.time()
st.write(load_data_a(csv_url))
a1 = time_module.time()
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

b0 = time_module.time()
st.write(load_data_b(csv_url))
b1 = time_module.time()
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
    time_module.sleep(5)
st.success("데이타로딩 완료!")

with st.spinner("전체 작업 진행중..."):
    progress = st.progress(0)
    status_text = st.empty()  #텍스트 덮어쓰기 용 공간확보
    for i in range(5):
        status_text.write(f"       Step {i+1}/5 : 데이터 준비중...   ")
        time_module.sleep(1)
        progress.progress((i+1)*20)
st.success("처리가 모두 끝났습니다")
        
# st.session_state()
st.title("⚽ Boared API앱")
st.sidebar.header('입력')
selected_type = st.sidebar.selectbox('활동 유형 선택', ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])
#https://bored-api.appbrewery.com/
suggested_activity_url = f"https://bored-api.appbrewery.com/filter?type={selected_type}"

try:
    json_data = requests.get(suggested_activity_url, timeout=5)
    json_data.raise_for_status()
    result = json_data.json()

    # /filter 엔드포인트는 리스트를 반환하므로 첫 번째 항목 사용
    if isinstance(result, list):
        suggested_activity = result[0]
    else:
        suggested_activity = result

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