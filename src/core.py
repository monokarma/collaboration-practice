import streamlit as st

APP_TITLE = "종강 대탈출"  # 임시 이름

GATES = [
    ("G1", "까다로운 출석봇"),
    ("G2", "청개구리 퀴즈"),
    ("G3", "수상한 강의 공지"),
    ("G4", "팀플 빌런과 협상"),
    ("G5", "고장난 계산기"),
    ("G6", "기말 범위 기억하기"),
    ("G7", "종강 버튼의 배신"),
]
GATE_IDS = [gid for gid, _ in GATES]
GATE_TITLES = dict(GATES)
FINAL_GATE = "G7"


def init_state():
    defaults = {
        "current": GATE_IDS[0],
        "cleared": {gid: False for gid in GATE_IDS},
        "clues": {},
        "gate_data": {gid: {} for gid in GATE_IDS},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def gate_data(gid):
    """관문 전용 저장 공간. 점수, 시도 횟수 등은 여기에 저장."""
    return st.session_state.gate_data[gid]


def complete_gate(gid, clue=None):
    """관문 통과 시 호출. clue는 G7에서 암호 검증에 쓸 단서."""
    st.session_state.cleared[gid] = True
    if clue is not None:
        st.session_state.clues[gid] = clue


def is_cleared(gid):
    return st.session_state.cleared[gid]


def all_cleared(exclude=(FINAL_GATE,)):
    """G7에서 '앞 관문을 모두 완료했는지' 확인할 때 사용."""
    return all(is_cleared(gid) for gid in GATE_IDS if gid not in exclude)


def get_clues():
    """G7에서 모인 단서를 확인할 때 사용."""
    return dict(st.session_state.clues)


def reset_gate(gid):
    """관문 하나만 재시작. 위젯 key가 'G1_'로 시작하면 같이 지워짐."""
    st.session_state.cleared[gid] = False
    st.session_state.clues.pop(gid, None)
    st.session_state.gate_data[gid] = {}
    for key in [k for k in st.session_state if str(k).startswith(f"{gid}_")]:
        del st.session_state[key]


def reset_all():
    """전체 초기화 (G7-B 종강 처리에서도 사용)."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()


def go(gid):
    st.session_state.current = gid
