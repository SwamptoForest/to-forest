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
target_team = st.selectbox("진출 확률이 궁금한 국가를 선택해:", df["국가"].tolist())
prob = df[df["국가"] == target_team]["진출 확률(%)"].values[0]

if prob > 90:
    st.success(f"**{target_team}**의 32강 진출 확률은 **{prob}%**야. 거의 확정이라고 봐야지!")
elif prob > 70:
    st.info(f"**{target_team}**의 진출 확률은 **{prob}%**로 꽤 높은 편이야.")
else:
    st.warning(f"**{target_team}**은 **{prob}%**로 쉽지 않은 여정이 되겠어.")
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



