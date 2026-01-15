import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    "국가": ["스페인", "아르헨티나", "브라질", "독일", "잉글랜드", "프랑스", "네덜란드", "멕시코", "대한민국", "미국", "노르웨이", "일본", "사우디아라비아", "남아공"],
    "조": ["H", "J", "C", "E", "L", "I", "F", "A", "A", "D", "I", "F", "H", "A"],
    "진출 확률(%)": [99.0, 99.0, 99.0, 99.0, 99.0, 96.0, 93.3, 88.2, 77.3, 85.2, 85.2, 73.7, 45.5, 38.5]
}

df = pd.DataFrame(data)

# 사이드바에서 조별 필터링 기능 추가
st.sidebar.header("필터 설정")
selected_group = st.sidebar.multiselect("확인하고 싶은 조를 선택해:", df["조"].unique(), default=df["조"].unique())

# 필터링된 데이터
filtered_df = df[df["조"].isin(selected_group)].sort_values(by="진출 확률(%)", ascending=False)

# 메인 화면 구성
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 국가별 진출 확률 데이터")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    
    st.subheader("📈 시각화 차트")
    df['국가_세로'] = df['국가'].apply(lambda x: '\n'.join(list(x))) #
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['국가_세로'], df['진출 확률(%)'], color='#ff4b4b')
    y_label = "진\n출\n확\n률\n(%)"
    ax.set_ylabel(y_label, rotation=0, labelpad=30, verticalalignment='center') # 축 이름도 세로로
    st.pyplot(fig, use_container_width=True)

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

