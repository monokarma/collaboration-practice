"""G4 팀플 빌런과 협상

G4-A: 빌런과 3번 협상하면서 선택할 때마다 점수를 갱신한다.
"""

import streamlit as st

from core import gate_data

GID = "G4"

# 선택지는 (보여 줄 문장, 점수) 묶음이다.
ROUNDS = [
    {
        "situation": "빌런: '저 이번 주 바빠서 자료조사는 못 할 것 같아요~'",
        "options": [
            ("알겠어요, 제가 대신 할게요.", 0),
            ("마감일을 정하고 분량을 줄여 드릴게요.", 2),
            ("단톡방에서 공개적으로 따진다.", -1),
        ],
    },
    {
        "situation": "빌런: '발표는 제가 할게요. 대신 PPT는 다른 분이...'",
        "options": [
            ("교수님께 바로 이른다.", -1),
            ("일단 넘어간다.", 0),
            ("발표 대본 초안까지 맡아 달라고 협상한다.", 2),
        ],
    },
    {
        "situation": "빌런: '깃허브는 어려워서 커밋은 안 할래요.'",
        "options": [
            ("PR 올리는 법을 같이 해 보자고 한다.", 2),
            ("커밋 기록이 없으면 기여도 0점이라고 알려 준다.", 1),
            ("빌런 몫까지 내가 커밋한다.", 0),
        ],
    },
]


def apply_choice(score, round_info, choice_no):
    """G4-A: 고른 선택지(1부터 시작)의 점수를 더한 새 점수를 돌려준다."""
    _, points = round_info["options"][choice_no - 1]
    return score + points


def play_rounds():
    """G4-A 화면. 한 라운드씩 선택을 받아 점수를 갱신한다.

    3라운드가 끝났으면 최종 점수를, 진행 중이면 None을 돌려준다.
    """
    data = gate_data(GID)
    data.setdefault("round", 0)  # 끝낸 라운드 수
    data.setdefault("score", 0)
    done = data["round"]
    score = data["score"]
    if done >= len(ROUNDS):
        return score

    r = ROUNDS[done]
    st.write(f"**[{done + 1}/{len(ROUNDS)}]** {r['situation']}")
    st.caption(f"현재 협상 점수: {score}점")
    choice = st.radio(
        "어떻게 대답할까요?",
        list(range(1, len(r["options"]) + 1)),
        index=None,
        format_func=lambda no: r["options"][no - 1][0],
        key=f"{GID}_choice_{done}",
    )
    if st.button("선택", key=f"{GID}_submit_{done}"):
        if choice is None:
            st.warning("선택지를 하나 고르세요.")
        else:
            data["score"] = apply_choice(score, r, choice)
            data["round"] = done + 1
            st.rerun()
    return None


def render():
    score = play_rounds()
    if score is not None:
        st.info(f"최종 협상 점수: {score}점")