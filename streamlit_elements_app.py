# 우리 애플리케이션에 필요한 다음의 임포트를 먼저 해야 합니다.

import json
import streamlit as st
from pathlib import Path

# Streamlit Elements에서는 다음의 객체들이 필요합니다.
# 모든 사용 가능한 객체와 그 사용법은 여기에 나와 있습니다: https://github.com/okld/streamlit-elements#getting-started

from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# 대시보드가 전체 페이지를 차지하도록 페이지 레이아웃을 변경합니다.

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("🗓️ #30DaysOfStreamlit")
    st.header("Day 27 - Streamlit Elements")
    st.write("Streamlit Elements를 사용하여 드래그 가능하고 크기 조절 가능한 대시보드 만들기.")
    st.write("---")

    # 미디어 플레이어에 대한 URL 정의.
    media_url = st.text_input("미디어 URL", value="https://www.youtube.com/watch?v=vIQQR_yq-8I")

# 코드 편집기와 차트에 대한 기본 데이터 초기화.
#
# 이 튜토리얼에서는 Nivo Bump 차트에 필요한 데이터가 필요합니다.
# 여기서 랜덤 데이터를 얻을 수 있습니다: https://nivo.rocks/bump/의 'data' 탭.
#
# 아래에서 보시다시피, 이 세션 상태 항목은 코드 편집기가 변경될 때 업데이트되며,
# Nivo Bump 차트가 데이터를 그리기 위해 읽을 것입니다.

if "data" not in st.session_state:
    st.session_state.data = (Path(__file__).parent / "data.json").read_text()

# 기본 대시보드 레이아웃을 정의합니다.
# 대시보드 그리드는 기본적으로 12개의 열을 가지고 있습니다.
#
# 사용 가능한 매개변수에 대한 자세한 정보:
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    # 편집기 항목은 x=0, y=0 좌표에 위치하며, 12/6열을 차지하고 높이는 3입니다.
    dashboard.Item("editor", 0, 0, 6, 3),
    # 차트 항목은 x=6, y=0 좌표에 위치하며, 12/6열을 차지하고 높이는 3입니다.
    dashboard.Item("chart", 6, 0, 6, 3),
    # 미디어 항목은 x=0, y=3 좌표에 위치하며, 12/6열을 차지하고 높이는 4입니다.
    dashboard.Item("media", 0, 2, 12, 4),
]

# 요소를 표시할 프레임을 만듭니다.

with elements("demo"):

    # 위에서 지정한 레이아웃으로 새 대시보드를 만듭니다.
    #
    # draggableHandle은 대시보드 항목의 드래그 가능한 부분을 정의하는 CSS 쿼리 선택자입니다.
    # 여기서는 'draggable' 클래스 이름을 가진 요소가 드래그 가능합니다.
    #
    # 대시보드 그리드에 사용 가능한 매개변수에 대한 자세한 정보:
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

    with dashboard.Grid(layout, draggableHandle=".draggable"):

        # 첫 번째 카드, 코드 편집기.
        #
        # 'key' 매개변수를 사용하여 올바른 대시보드 항목을 식별합니다.
        #
        # 카드 콘텐츠가 자동으로 사용 가능한 높이를 채우도록 하려면 CSS flexbox를 사용합니다.
        # sx는 모든 Material UI 위젯에서 CSS 속성을 정의하는 데 사용할 수 있는 매개변수입니다.
        #
        # 카드, flexbox 및 sx에 대한 자세한 정보:
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/

        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

            # 이 헤더를 드래그 가능하게 만들려면 위의 dashboard.Grid의 draggableHandle에 정의된 대로
            # 클래스 이름을 'draggable'로 설정하기만 하면 됩니다.

            mui.CardHeader(title="Editor", className="draggable")

            # 여기서는 카드 콘텐츠가 사용자가 카드를 줄일 때 줄어들고 사용 가능한 모든 높이를 차지하도록 하기 위해
            # flex를 1로, minHeight를 0으로 설정합니다.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # 여기에 우리의 Monaco 코드 편집기가 있습니다.
                #
                # 먼저, st.session_state.data에 초기화한 기본값을 설정합니다.
                # 두 번째로, 사용할 언어를 JSON으로 정의합니다.
                #
                # 그런 다음, 편집기 콘텐츠에 대한 변경 사항을 검색하려고 합니다.
                # Monaco 문서를 확인하면 onChange 속성이 함수를 사용한다는 것을 알 수 있습니다.
                # 이 함수는 변경이 이루어질 때마다 호출되며, 업데이트된 콘텐츠 값이 첫 번째 매개변수로 전달됩니다.
                # (cf. onChange: https://github.com/suren-atoyan/monaco-react#props)
                #
                # Streamlit Elements는 Streamlit의 세션 상태 항목으로 매개변수를 자동으로 전달하는 콜백을 만드는
                # 특별한 sync() 함수를 제공합니다.
                #
                # 예시
                # --------
                # 첫 번째 매개변수를 "data"라는 세션 상태 항목으로 전달하는 콜백을 생성
                # >>> editor.Monaco(onChange=sync("data"))
                # >>> print(st.session_state.data)
                #
                # 두 번째 매개변수를 "ev"라는 세션 상태 항목으로 전달하는 콜백을 생성
                # >>> editor.Monaco(onChange=sync(None, "ev"))
                # >>> print(st.session_state.ev)
                #
                # 두 매개변수 모두 세션 상태로 전달하는 콜백을 생성
                # >>> editor.Monaco(onChange=sync("data", "ev"))
                # >>> print(st.session_state.data)
                # >>> print(st.session_state.ev)
                #
                # onChange는 변경이 발생할 때마다 호출되므로, 단일 문자를 입력할 때마다
                # 전체 Streamlit 앱이 다시 실행되는 문제가 있습니다.
                #
                # 이 문제를 피하기 위해 다른 이벤트(예: 버튼 클릭)가 발생할 때까지 업데이트된 데이터를 보내도록
                # Streamlit Elements에게 지시할 수 있습니다. 이는 lazy()로 콜백을 감싸는 것으로 할 수 있습니다.
                #
                # Monaco에 사용 가능한 매개변수에 대한 자세한 정보:
                # https://github.com/suren-atoyan/monaco-react
                # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

                editor.Monaco(
                    defaultValue=st.session_state.data,
                    language="json",
                    onChange=lazy(sync("data"))
                )

            with mui.CardActions:

                # Monaco 편집기에는 lazy 콜백이 onChange에 바인딩되어 있으므로, Monaco의 내용을 변경해도
                # Streamlit은 직접 알림을 받지 못하고, 따라서 단일 문자를 입력할 때마다 다시 로드되지 않습니다.
                # 그래서 다른 비-lazy 이벤트가 업데이트를 트리거할 필요가 있습니다.
                #
                # 해결책은 클릭 시 콜백을 발생시키는 버튼을 생성하는 것입니다.
                # 콜백은 특별히 할 일이 없어도 됩니다. 빈 파이썬 함수를 생성하거나, 아무런 인수 없이 sync()를
                # 사용할 수 있습니다.
                #
                # 이제, 이 버튼을 클릭할 때마다 onClick 콜백이 발생하지만, 그 사이에 변경된 다른 모든 lazy
                # 콜백도 호출됩니다.

                mui.Button("변경 사항 적용", onClick=sync())

        # 두 번째 카드, Nivo Bump 차트.
        # 첫 번째 카드와 동일한 flexbox 구성을 사용하여 콘텐츠 높이를 자동으로 조정합니다.

        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

            # 이 헤더를 드래그 가능하게 만들려면, 위의 dashboard.Grid의 draggableHandle에 정의된 대로
            # 클래스 이름을 'draggable'로 설정하기만 하면 됩니다.

            mui.CardHeader(title="차트", className="draggable")

            # 위와 같이, 사용자가 카드 크기를 조절할 때 콘텐츠가 자동으로 늘어나고 줄어들도록 하기 위해
            # flex를 1로, minHeight를 0으로 설정합니다.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # 여기서 Bump 차트를 그립니다.
                #
                # 이번 연습에서는 Nivo의 예제를 가져와 Streamlit Elements에서 작동하도록 조정할 수 있습니다.
                # Nivo의 예제는 여기 'code' 탭에서 찾을 수 있습니다: https://nivo.rocks/bump/
                #
                # 데이터는 딕셔너리 형식의 매개변수를 취하므로, `json.loads()`를 사용하여
                # JSON 데이터를 문자열에서 파이썬 딕셔너리로 변환해야 합니다.
                #
                # 다른 Nivo 차트에 대한 자세한 정보는 다음 주소에서 확인할 수 있습니다.
                # https://nivo.rocks/

                nivo.Bump(
                    data=json.loads(st.session_state.data),
                    colors={ "scheme": "spectral" },
                    lineWidth=3,
                    activeLineWidth=6,
                    inactiveLineWidth=3,
                    inactiveOpacity=0.15,
                    pointSize=10,
                    activePointSize=16,
                    inactivePointSize=0,
                    pointColor={ "theme": "background" },
                    pointBorderWidth=3,
                    activePointBorderWidth=3,
                    pointBorderColor={ "from": "serie.color" },
                    axisTop={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": -36
                    },
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": 32
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "ranking",
                        "legendPosition": "middle",
                        "legendOffset": -40
                    },
                    margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                    axisRight=None,
                )

        # 대시보드의 세 번째 요소, 미디어 플레이어.

        with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="미디어 플레이어", className="draggable")
            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # 이 요소는 ReactPlayer에 의해 구동되며, YouTube 외에도 많은 플레이어를 지원합니다.
                # 여기에서 확인할 수 있습니다: https://github.com/cookpete/react-player#props

                media.Player(url=media_url, width="100%", height="100%", controls=True)

# 비동기/멀티스레딩 미지원 --> 지원으로 발전함(현재)
# 모듈화/컴포넌트 구조 부족 --> 지원으로 발전함(현재)
# 다이나믹 네비게이션 구현 가능
# LLM, CHAT하는 것도 구현이 가능되어짐
# Cashing, ~~~ 등등 docementation에서 잘~~ 살펴서 해보셩
# 라우팅 기능 가능해짐
# 모바일 최적화는 되어져 있으나, 브러우저에서만 표시됨