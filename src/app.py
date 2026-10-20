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


# ─────────────────────────────────────────
# 공용 상태 & 헬퍼 (모든 관문이 이걸로 소통)
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "current": GATE_IDS[0],
        "cleared": {gid: False for gid in GATE_IDS},
        "clues": {},  # 관문별 단서 (G7 암호 검증용)
        "gate_data": {gid: {} for gid in GATE_IDS},  # 관문별 전용 저장 공간
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


def reset_gate(gid):
    """관문 하나만 재시작. 위젯 key는 'G1_xxx'처럼 관문 ID로 시작하게 만들 것."""
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


# ─────────────────────────────────────────
# 관문 연결부: 구현이 끝나면 여기에 render 함수만 꽂으면 됨
# ─────────────────────────────────────────
def render_stub(gid):
    st.info(f"🚧 {gid}-A / {gid}-B 는 아직 연결되지 않았어요.")
    st.button(
        "(개발용) 이 관문 완료 처리",
        key=f"{gid}_dev_clear",
        on_click=complete_gate,
        args=(gid, f"{gid}-CLUE"),
    )


RENDERERS = {
    # "G1": g1.render,
    # "G2": g2.render,
}


# ─────────────────────────────────────────
# 화면
# ─────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, page_icon="🎓")
init_state()

with st.sidebar:
    st.title(f"🎓 {APP_TITLE}")
    done = sum(st.session_state.cleared.values())
    st.progress(done / len(GATE_IDS), text=f"{done} / {len(GATE_IDS)} 관문 완료")
    st.radio(
        "관문",
        GATE_IDS,
        key="current",
        format_func=lambda g: f"{'✅' if is_cleared(g) else '⬜'} {g} {GATE_TITLES[g]}",
    )
    st.divider()
    st.button("🔄 전체 초기화", on_click=reset_all)
    with st.expander("🛠 디버그"):
        st.write("완료:", st.session_state.cleared)
        st.write("단서:", st.session_state.clues)

cur = st.session_state.current
st.header(f"{cur} · {GATE_TITLES[cur]}")

if is_cleared(cur):
    st.success("통과한 관문이에요.")

render = RENDERERS.get(cur)
if render:
    render()
else:
    render_stub(cur)

st.divider()
col1, col2 = st.columns(2)
col1.button("↺ 이 관문 다시 하기", on_click=reset_gate, args=(cur,))
idx = GATE_IDS.index(cur)
if is_cleared(cur) and idx + 1 < len(GATE_IDS):
    col2.button("다음 관문 →", on_click=go, args=(GATE_IDS[idx + 1],))
