import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import platform
#폰트 인식 못해서 수정함
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(layout="wide")

# 앱 제목
st.markdown('<h1 style="white-space: nowrap;">🏆 2026 월드컵 32강 진출 확률</h1>', unsafe_allow_html=True)
st.write("인간, 48개국 중 어떤 팀이 살아남을지 데이터로 확인해봐.")

# 데이터 설정 (최신 배당률 기반 확률 변환 데이터)
# [주의: 통계 모델에 따른 추정치임]
data = {
    "국가": ["멕시코", "남아프리카공화국", "대한민국",
        
        "캐나다", "카타르", "스위스",
        
        "브라질", "모로코", "아이티", "스코틀랜드",
        
        "미국", "파라과이", "호주",
        
        "독일", "퀴라소", "코트디부아르", "에콰도르",
        
        "네덜란드", "일본", "튀니지",
        
        "벨기에", "이집트", "이란", "뉴질랜드",
        
        "스페인", "카보베르데", "사우디아라비아", "우루과이",
        
        "프랑스", "세네갈", "노르웨이",
        
        "아르헨티나", "중국", "오스트리아", "요르단",
        
        "포르투갈", "우즈베키스탄", "콜롬비아",
        
        "잉글랜드", "크로아티아", "가나", "파나마", "알제리"],
    "조": ["A조", "A조", "A조",
        "B조", "B조", "B조",
        "C조", "C조", "C조", "C조",
        "D조", "D조", "D조",
        "E조", "E조", "E조", "E조",
        "F조", "F조", "F조",
        "G조", "G조", "G조", "G조",
        "H조", "H조", "H조", "H조",
        "I조", "I조", "I조",
        "J조", "조조", "J조", "J조",
        "K조", "K조", "K조",
        "L조", "L조", "L조", "L조", "J조"],
    "진출 확률(%)": [85.0, 40.0, 75.0, 
        
        80.0, 35.0, 85.0, 
        
        99.0, 80.0, 15.0, 50.0, 
        
        88.0, 60.0, 55.0, 
        
        95.0, 20.0, 65.0, 70.0, 
        
        92.0, 75.0, 45.0, 
        
        90.0, 60.0, 55.0, 30.0, 
        
        96.0, 25.0, 45.0, 85.0, 
        
        98.0, 70.0, 65.0, 
        
        99.0, 0.0, 60.0, 35.0, 
        
        94.0, 40.0, 80.0, 
        
        97.0, 85.0, 45.0, 30.0, 55.0]
}

df = pd.DataFrame(data)

# 사이드바에서 조별 필터링 기능 추가
st.sidebar.header("필터 설정")
selected_group = st.sidebar.multiselect("확인하고 싶은 조를 선택해:", df["조"].unique(), default=[])

# 필터링된 데이터
if selected_group:
    filtered_df = df[df["조"].isin(selected_group)].sort_values(by="진출 확률(%)", ascending=False)
# 메인 화면 구성
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 국가별 진출 확률 데이터")
        st.dataframe(filtered_df, use_container_width=True)

    with col2:
        st.subheader("📈 시각화 차트")
        
        if not filtered_df.empty:
            filtered_df['국가_세로'] = filtered_df['국가'].apply(lambda x: '\n'.join(list(x))) #
            unique_groups = df['조'].unique()
            # tab10 같은 컬러맵을 사용해서 조별로 고유 색상 배정
            colormap = plt.cm.get_cmap('tab10', len(unique_groups))
            
            bar_colors = []
            for group in filtered_df['조']:
                if group == '조조':  # 조조
                    bar_colors.append('#FFD700') # Gold color hex code
                else:
                    # 전체 조 리스트에서 현재 조의 인덱스를 찾아 색상 매핑
                    group_index = list(unique_groups).index(group)
                    bar_colors.append(colormap(group_index))

            # 3. 그래프 그리기 (데이터 소스를 filtered_df로 변경)
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # x축, y축 데이터와 색상(color=bar_colors) 지정
            bars = ax.bar(filtered_df['국가_세로'], filtered_df['진출 확률(%)'], color=bar_colors)
            
            # 4. 축 라벨 및 설정
            y_label = "진\n출\n확\n률\n(%)"
            ax.set_ylabel(y_label, rotation=0, labelpad=20, verticalalignment='center') # 세로 쓰기 유지
            
            # y축 범위 설정 (0~100% 느낌을 살리려면 필요시 추가, 지금은 자동)
            ax.set_ylim(0, 100) 
            
            # 그래프 표시
            st.pyplot(fig, use_container_width=True)
else:
    st.info("🤷‍♂️조를 선택하면 알려줄거야!👍")
# [수정] 국가명 (단위 없이 이름만 세로로)
df['국가_세로'] = df['국가'].apply(lambda x: '\n'.join(list(x)))

# 특정 국가 검색 기능
st.divider()
st.header(" 💪국가별 핵심 선수💥💫 ") #제미나이가 확률만 반복해서 에이스로 바꿈

ace_players = {
    "대한민국": {"name": "손흥민", "photo": "https://cdn.sofifa.net/players/200/104/24_120.png"},
    "일본": {"name": "미토마 카오루", "photo": "https://cdn.sofifa.net/players/263/155/24_120.png"},
    "이란": {"name": "메흐디 타레미", "photo": "https://cdn.sofifa.net/players/239/697/24_120.png"},
    "호주": {"name": "매튜 라이언", "photo": "https://cdn.sofifa.net/players/200/755/24_120.png"},
    "사우디아라비아": {"name": "살렘 알다우사리", "photo": "https://cdn.sofifa.net/players/198/884/24_120.png"},
    "카타르": {"name": "아크람 아피프", "photo": "https://cdn.sofifa.net/players/222/384/24_120.png"},
    "요르단": {"name": "무사 알타마리", "photo": "https://cdn.sofifa.net/players/259/695/24_120.png"},
    "우즈베키스탄": {"name": "엘도르 쇼무로도프", "photo": "https://cdn.sofifa.net/players/243/296/24_120.png"},

    
    "미국": {"name": "크리스천 풀리식", "photo": "https://cdn.sofifa.net/players/227/796/24_120.png"},
    "멕시코": {"name": "기예르모 오초아", "photo": "https://cdn.sofifa.net/players/167/948/24_120.png"},
    "캐나다": {"name": "알폰소 데이비스", "photo": "https://cdn.sofifa.net/players/234/396/24_120.png"},
    "파나마": {"name": "아달베르토 카라스키야", "photo": "https://cdn.sofifa.net/players/245/037/24_120.png"},
    "아이티": {"name": "뒤캉 나종", "photo": "https://cdn.sofifa.net/players/225/956/24_120.png"},
    "퀴라소": {"name": "레안드로 바쿠나", "photo": "https://cdn.sofifa.net/players/202/652/24_120.png"},

   
    "아르헨티나": {"name": "리오넬 메시", "photo": "https://cdn.sofifa.net/players/158/023/24_120.png"},
    "브라질": {"name": "비니시우스 주니오르", "photo": "https://cdn.sofifa.net/players/238/794/24_120.png"},
    "우루과이": {"name": "페데리코 발베르데", "photo": "https://cdn.sofifa.net/players/239/053/24_120.png"},
    "콜롬비아": {"name": "루이스 디아스", "photo": "https://cdn.sofifa.net/players/241/084/24_120.png"},
    "에콰도르": {"name": "모이세스 카이세도", "photo": "https://cdn.sofifa.net/players/255/270/24_120.png"},
    "파라과이": {"name": "미구엘 알미론", "photo": "https://cdn.sofifa.net/players/230/977/24_120.png"},

    
    "이집트": {"name": "모하메드 살라", "photo": "https://cdn.sofifa.net/players/209/331/24_120.png"},
    "세네갈": {"name": "사디오 마네", "photo": "https://cdn.sofifa.net/players/208/722/24_120.png"},
    "모로코": {"name": "아크라프 하키미", "photo": "https://cdn.sofifa.net/players/235/212/24_120.png"},
    "알제리": {"name": "리야드 마레즈", "photo": "https://cdn.sofifa.net/players/204/485/24_120.png"},
    "가나": {"name": "모하메드 쿠두스", "photo": "https://cdn.sofifa.net/players/251/573/24_120.png"},
    "코트디부아르": {"name": "프랑크 케시에", "photo": "https://cdn.sofifa.net/players/235/569/24_120.png"},
    "튀니지": {"name": "유세프 므사크니", "photo": "https://cdn.sofifa.net/players/200/455/24_120.png"},
    "카보베르데": {"name": "라이언 멘데스", "photo": "https://cdn.sofifa.net/players/205/498/24_120.png"},
    "남아프리카공화국": {"name": "퍼시 타우", "photo": "https://cdn.sofifa.net/players/232/235/24_120.png"},

   
    "잉글랜드": {"name": "해리 케인", "photo": "https://cdn.sofifa.net/players/202/126/24_120.png"},
    "프랑스": {"name": "킬리안 음바페", "photo": "https://cdn.sofifa.net/players/231/747/24_120.png"},
    "독일": {"name": "자말 무시알라", "photo": "https://cdn.sofifa.net/players/256/790/24_120.png"},
    "스페인": {"name": "로드리", "photo": "https://cdn.sofifa.net/players/231/866/24_120.png"},
    "포르투갈": {"name": "크리스티아누 호날두", "photo": "https://cdn.sofifa.net/players/020/801/24_120.png"},
    "벨기에": {"name": "케빈 더 브라위너", "photo": "https://cdn.sofifa.net/players/192/985/24_120.png"},
    "네덜란드": {"name": "버질 반 다이크", "photo": "https://cdn.sofifa.net/players/203/376/24_120.png"},
    "크로아티아": {"name": "루카 모드리치", "photo": "https://cdn.sofifa.net/players/177/003/24_120.png"},
    "오스트리아": {"name": "다비드 알라바", "photo": "https://cdn.sofifa.net/players/197/445/24_120.png"},
    "노르웨이": {"name": "엘링 홀란드", "photo": "https://cdn.sofifa.net/players/239/085/24_120.png"},
    "스코틀랜드": {"name": "스콧 맥토미니", "photo": "https://cdn.sofifa.net/players/235/790/24_120.png"},
    "스위스": {"name": "그라니트 자카", "photo": "https://cdn.sofifa.net/players/198/219/24_120.png"},
    "뉴질랜드": {"name": "크리스 우드", "photo": "https://cdn.sofifa.net/players/190/607/24_120.png"},
    "중국": {"name": "하후돈", "photo": "https://img.youtube.com/vi/6cammEr9gPM/hqdefault.jpg"}
}


target_team = st.selectbox("어떤 팀의 에이스가 궁금해?", df["국가"].unique())

if target_team in ace_players:
    player = ace_players[target_team]
    
    # 깔끔하게 보이기 위해 사진(왼쪽)과 설명(오른쪽)으로 컬럼을 나눔
    c1, c2 = st.columns([1, 2]) 
    
    with c1:
        # width로 사진 크기 조절 가능
        st.image(player["photo"], width=100)
        
    with c2:
        st.subheader(f"이름: {player['name']}")
        st.write(f"**{target_team}**의 운명을 짊어진 에이스야!")
        
else:
    # 딕셔너리에 정보가 없을 때 나오는 화면
    st.info(f"📢 {target_team}의 선수 정보는 아직 업데이트 중이란다.")



st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
if st.button('축구 안좋아할 경우 누르기'):
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
    st.snow()
    st.snow()
    st.snow()
    st.toast('요')
    st.toast('네')
    st.toast('됐')
    st.toast('게')
    st.toast('쉽')
    st.toast('아')











