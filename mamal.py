import streamlit as st
import requests # 선수 사진이 자꾸 엑박이라서 제미나이를 압박했더니 해결책이라고 준 것.
from PIL import Image # 엑박 해결용 2, 이거는 저 윗녀석이 가져온 데이터를 이미지로 변환시켜준다는 라이브러리.
from io import BytesIO # 엑박 해결용 3. 이거는 가져온 데이터를 일일이 컴퓨터에 저장하고 다시 변환하고 이러면 느려지니까 중간에 가상의 저장위치 역할을 해서 과정을 간소하게 해준다 함.
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
def load_image(url): # 얘가 위에서 가져온 라이브러리들을 막 섞어쓰면서 사진을 온전히 모셔오게 하려고 만든 함수(제미나이가 만듬)
    try:
        # "나 봇 아니고 윈도우 쓰는 사람이야~"라고 속이는 명찰(Header) # 참고로 내가 단 주석과 제미나이가 설명해준다고 단 주석이 마구 섞여있음.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        return None # 실패하면 아무것도 안 돌려줌

st.divider()
st.header(" 💪국가별 핵심 선수💥💫 ") #제미나이가 확률만 반복해서 에이스로 바꿈

ace_players = {
    "대한민국": {"name": "손흥민", "photo": "https://i.namu.wiki/i/GgC0j0JqZ4G4a9x5_q3y5a2k_7l0y5x7.jpg"}, # 믿고 쓰는 쏘니
    "일본": {"name": "미토마 카오루", "photo": "https://img.olympics.com/images/image/private/t_s_pog_staticContent_hero_xl_2x/f_auto/primary/pog1q1q1q1q1q1q1q1q1"}, # 드리블 돌파 장면
    "호주": {"name": "매튜 라이언", "photo": "https://resources.premierleague.com/premierleague/photos/players/250x250/p109533.png"}, # 듬직한 골키퍼
    "이란": {"name": "메흐디 타레미", "photo": "https://i2-prod.mirror.co.uk/incoming/article31940907.ece/ALTERNATES/s1200c/0_Mehdi-Taremi.jpg"}, # 골 세리머니
    "사우디아라비아": {"name": "살렘 알다우사리", "photo": "https://i.dailymail.co.uk/1s/2022/11/22/11/64789645-11456383-image-a-1_1669115456257.jpg"}, # 아르헨전 역전골 환호
    "카타르": {"name": "아크람 아피프", "photo": "https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/bltf7c126601438903c/65c8a07f0b5d03040a439225/Akram_Afif_Qatar_Asian_Cup_2023.jpg"}, # 아시안컵 하드캐리
    "요르단": {"name": "무사 알타마리", "photo": "https://images.ps-aws.com/c?url=https%3A%2F%2Fimages.daznservices.com%2Fdi%2Flibrary%2FGOAL%2F62%2F67%2Fmusa-al-taamari-jordan-asian-cup-2023_176313i2b4j211a7y0j028j091.jpg"}, # 요르단 메시 드리블
    "우즈베키스탄": {"name": "엘도르 쇼무로도프", "photo": "https://as01.epimg.net/en/imagenes/2024/01/16/soccer/1705423871_507641_1705424003_noticia_normal.jpg"}, # 국대 캡틴 포스

    # [북중미] - 멕시코 오초아 수정!
    "멕시코": {"name": "기예르모 오초아", "photo": "https://cdn.vox-cdn.com/thumbor/M7W-z5E5qgM8-q_Z5qM5-q_Z5qM=/0x0:3000x2000/1200x800/filters:focal(1260x880:1740x1360)/cdn.vox-cdn.com/uploads/chorus_image/image/71676662/1443666666.0.jpg"}, # 월드컵의 남자, 선방쇼
    "미국": {"name": "크리스천 풀리식", "photo": "https://cdn.cnn.com/cnnnext/dam/assets/221129150338-01-christian-pulisic-goal-iran-restricted-super-tease.jpg"}, # 골 넣는 장면
    "캐나다": {"name": "알폰소 데이비스", "photo": "https://i.cbc.ca/1.6666060.1669566666!/fileImage/httpImage/image.jpg_gen/derivatives/16x9_780/alphonso-davies-goal-croatia.jpg"}, # 역사적인 첫 골
    "파나마": {"name": "아달베르토 카라스키야", "photo": "https://bolavip.com/__export/1689283738686/sites/bolavip/img/2023/07/13/adalberto_carrasquilla_panama_semifinal_copa_oro_2023.jpg_1159711837.jpg"},
    "아이티": {"name": "뒤캉 나종", "photo": "https://haititempo.com/wp-content/uploads/2019/06/Duckens-Nazon-Gold-Cup-2019.jpg"},
    "퀴라소": {"name": "레안드로 바쿠나", "photo": "https://knvb-images.imgix.net/dam/3b/6e/3b6e8a8a-7e6e-4e6e-8e6e-3b6e8a8a7e6e.jpg"},

    # [남미] - 에콰도르 추가
    "아르헨티나": {"name": "리오넬 메시", "photo": "https://image.chosun.com/sitedata/image/202212/19/2022121900138_0.jpg"}, # 월드컵 우승 트로피 키스
    "브라질": {"name": "비니시우스 주니오르", "photo": "https://i2-prod.manchestereveningnews.co.uk/incoming/article25686662.ece/ALTERNATES/s1200c/0_GettyImages-1443666666.jpg"},
    "에콰도르": {"name": "모이세스 카이세도", "photo": "https://i2-prod.football.london/incoming/article27514332.ece/ALTERNATES/s1200c/0_GettyImages-1585666666.jpg"}, # 첼시/국대 중원 장악
    "우루과이": {"name": "페데리코 발베르데", "photo": "https://img.hankyung.com/photo/202211/01.31914948.1.jpg"}, # 강렬한 중거리 슛 자세
    "콜롬비아": {"name": "루이스 디아스", "photo": "https://i.guim.co.uk/img/media/3b6e8a8a7e6e4e6e8e6e3b6e8a8a7e6e/0_0_3000_2000/master/3000.jpg?width=1200&quality=85&auto=format&fit=max&s=3b6e8a8a7e6e4e6e8e6e3b6e8a8a7e6e"},
    "파라과이": {"name": "미구엘 알미론", "photo": "https://i2-prod.chroniclelive.co.uk/incoming/article25345678.ece/ALTERNATES/s1200c/0_Miguel-Almiron.jpg"},

    # [유럽] - 스코틀랜드 수정!
    "스코틀랜드": {"name": "스콧 맥토미니", "photo": "https://i2-prod.dailyrecord.co.uk/incoming/article29574321.ece/ALTERNATES/s1200c/0_Scott-McTominay-Scotland.jpg"}, # 스코틀랜드 유니폼 입고 포효
    "잉글랜드": {"name": "해리 케인", "photo": "https://i.skysports.com/23/03/768x432/skysports-harry-kane-england_6097566.jpg"},
    "프랑스": {"name": "킬리안 음바페", "photo": "https://cdn.theathletic.com/app/uploads/2022/12/18113227/Mbappe-France-World-Cup-Final-2022-scaled-e1671381178656.jpg"},
    "포르투갈": {"name": "크리스티아누 호날두", "photo": "https://img.sbs.co.kr/newimg/news/20221125/201725538_1280.jpg"}, # 호우 세리머니 근접
    "독일": {"name": "자말 무시알라", "photo": "https://static.independent.co.uk/2022/11/27/21/GettyImages-1444987654.jpg"},
    "스페인": {"name": "로드리", "photo": "https://i2-prod.manchestereveningnews.co.uk/incoming/article27101234.ece/ALTERNATES/s1200c/0_Rodri-Spain.jpg"},
    "벨기에": {"name": "케빈 더 브라위너", "photo": "https://i.eurosport.com/2022/11/23/3495866-71264488-2560-1440.jpg"},
    "네덜란드": {"name": "버질 반 다이크", "photo": "https://images.teamtalk.com/content/uploads/2022/12/Virgil-van-Dijk-Netherlands.jpg"},
    "크로아티아": {"name": "루카 모드리치", "photo": "https://cdn.vox-cdn.com/thumbor/M7W-z5E5qgM8-q_Z5qM5-q_Z5qM=/0x0:3000x2000/1200x800/filters:focal(1260x880:1740x1360)/cdn.vox-cdn.com/uploads/chorus_image/image/71676662/1443666666.0.jpg"},
    "노르웨이": {"name": "엘링 홀란드", "photo": "https://cdn.theathletic.com/app/uploads/2023/06/17150000/Haaland-Norway-scaled.jpg"},
    "오스트리아": {"name": "다비드 알라바", "photo": "https://i.bundesliga.com/json/imap/media/2021/06/16/00000000-0000-0000-0000-000000000000_original.jpeg"},
    "스위스": {"name": "그라니트 자카", "photo": "https://i2-prod.football.london/incoming/article25686662.ece/ALTERNATES/s1200c/0_GettyImages-1443666666.jpg"},

    # [오세아니아 - 뉴질랜드 수정]
    "뉴질랜드": {"name": "크리스 우드", "photo": "https://resources.premierleague.com/premierleague/photos/players/250x250/p54469.png"}, # 프리미어리그 프로필
    "중국": {"name": "하후돈", "photo": "https://img.youtube.com/vi/6cammEr9gPM/hqdefault.jpg"}
}



target_team = st.selectbox("어떤 팀의 에이스가 궁금해?", df["국가"].unique())

if target_team in ace_players:
    player = ace_players[target_team]
    
    c1, c2 = st.columns([1, 2]) 
    
    with c1:
        # [수정] 그냥 url을 넣는 게 아니라, 함수로 이미지를 가져와서 넣음
        image_data = load_image(player["photo"])
        
        if image_data:
            st.image(image_data, width= 650)
        else:
            # 이미지를 못 가져왔을 때 보여줄 대체 텍스트나 아이콘
            st.error("이미지 로딩 실패")
        
    with c2:
        st.subheader(f"이름: {player['name']}")
        st.write(f"**{target_team}**의 운명을 짊어진 에이스야!")
        
else:
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













