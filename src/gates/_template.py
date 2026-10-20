import streamlit as st

from core import complete_gate, gate_data

GID = "G1"  # 자기 관문 ID로 변경


def render():
    data = gate_data(GID)  # 예: data["score"] = 0
    st.write("여기에 관문 화면을 구현하세요.")

    if st.button("제출", key=f"{GID}_submit"):  # 위젯 key는 GID_ 로 시작
        passed = True  # TODO: A 기능 판정 로직
        if passed:
            complete_gate(GID, clue="단서")  # TODO: 실제 단서
            st.rerun()  # 사이드바 체크 표시를 바로 반영
