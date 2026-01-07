import streamlit as st
import random
import time
import pandas as pd

# 1. 페이지 설정 및 스타일
st.set_page_config(page_title="올인원 플레이그라운드", page_icon="🌟", layout="wide")

# 2. 사이드바 메뉴 구성
with st.sidebar:
    st.title("🚀 멀티 앱 메뉴")
    selected = st.radio("이동할 페이지를 선택하세요", 
                        ["홈 화면", "자리 배치기", "숫자 맞추기 게임", "우주선 피하기", "행운의 룰렛"])
    st.divider()
    st.info("하나의 코드로 통합된 사이트입니다.")

# --- 1. 홈 화면 ---
if selected == "홈 화면":
    st.title("🏠 올인원 플레이그라운드")
    st.subheader("여러가지 도구와 게임을 한 곳에서 즐겨보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🛠️ 제공 도구")
        st.write("- **자리 배치기**: 랜덤 좌석 배정")
        st.write("- **행운의 룰렛**: 무작위 항목 추첨")
    with col2:
        st.write("### 🎮 미니 게임")
        st.write("- **숫자 맞추기**: Up & Down 퀴즈")
        st.write("- **우주선 피하기**: 버튼으로 즐기는 회피 게임")

# --- 2. 자리 배치기 ---
elif selected == "자리 배치기":
    st.title("🪑 랜덤 자리 배치기")
    input_names = st.text_area("명단을 입력하세요 (엔터로 구분)", height=150)
    cols_count = st.number_input("한 줄 인원수", 1, 10, 3)
    
    if st.button("배치 시작", type="primary"):
        if input_names.strip():
            names = [n.strip() for n in input_names.split('\n') if n.strip()]
            random.shuffle(names)
            rows = [names[i:i + cols_count] for i in range(0, len(names), cols_count)]
            for row in rows:
                cols = st.columns(cols_count)
                for i, name in enumerate(row):
                    cols[i].success(f"**{name}**")
        else:
            st.warning("이름을 입력해주세요.")

# --- 3. 숫자 맞추기 게임 ---
elif selected == "숫자 맞추기 게임":
    st.title("🎮 숫자 맞추기 (Up & Down)")
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)
        st.session_state.count = 0

    guess = st.number_input("1~100 사이 숫자", 1, 100)
    if st.button("확인"):
        st.session_state.count += 1
        if guess < st.session_state.target:
            st.warning("📈 UP!")
        elif guess > st.session_state.target:
            st.info("📉 DOWN!")
        else:
            st.balloons()
            st.success(f"🎉 정답! {st.session_state.count}번 만에 맞췄습니다.")
            if st.button("다시 시작"):
                del st.session_state.target
                st.rerun()

# --- 4. 우주선 피하기 ---
elif selected == "우주선 피하기":
    st.title("🚀 우주선 피하기")
    if 'p_pos' not in st.session_state:
        st.session_state.p_pos = 1
        st.session_state.obs_pos = random.randint(0, 2)
        st.session_state.score = 0

    st.subheader(f"Score: {st.session_state.score}")
    
    # 간단한 그래픽 표현
    lanes = ["   ", "   ", "   "]
    obs_lanes = ["   ", "   ", "   "]
    lanes[st.session_state.p_pos] = "🚀"
    obs_lanes[st.session_state.obs_pos] = "☄️"
    
    st.code(f"장애물: {' | '.join(obs_lanes)}\n우주선: {' | '.join(lanes)}")

    c1, c2, c3 = st.columns(3)
    move = None
    if c1.button("⬅️ 왼쪽"): move = 0
    if c2.button("⏺ 제자리"): move = st.session_state.p_pos
    if c3.button("➡️ 오른쪽"): move = 2

    if move is not None:
        st.session_state.p_pos = move
        if st.session_state.p_pos == st.session_state.obs_pos:
            st.error(f"💥 충돌! 점수: {st.session_state.score}")
            st.session_state.score = 0
        else:
            st.session_state.score += 1
        st.session_state.obs_pos = random.randint(0, 2)
        st.rerun()

# --- 5. 행운의 룰렛 ---
elif selected == "행운의 룰렛":
    st.title("🎡 행운의 룰렛")
    items_input = st.text_area("항목 입력 (쉼표 또는 엔터)", "짜장면, 짬뽕, 피자")
    items = [i.strip() for i in items_input.replace(',', '\n').split('\n') if i.strip()]
    
    if st.button("룰렛 돌리기!!"):
        if items:
            with st.status("추첨 중...", expanded=True) as status:
                for _ in range(10):
                    st.write(f"🎲 {random.choice(items)}")
                    time.sleep(0.1)
                result = random.choice(items)
                status.update(label="추첨 완료!", state="complete")
            st.subheader(f"🎉 결과는: **{result}**")
            st.balloons()
        else:
            st.error("항목을 입력하세요.")
