import importlib

import streamlit as st

from core import (
    APP_TITLE,
    GATE_IDS,
    GATE_TITLES,
    init_state,
    is_cleared,
    complete_gate,
    reset_gate,
    reset_all,
    go,
)


def load_renderer(gid):
    """gates/g1.py 같은 파일이 있으면 그 안의 render()를 가져옴. 없으면 None."""
    module_name = f"gates.{gid.lower()}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        if e.name in (module_name, "gates"):  # 파일이 아직 없을 때만 스텁으로 대체
            return None
        raise  # 관문 파일 안의 import 오류는 그대로 보여줌
    return getattr(module, "render", None)


def render_stub(gid):
    st.info(f"🚧 gates/{gid.lower()}.py 가 아직 없어요.")
    st.button(
        "(개발용) 이 관문 완료 처리",
        key=f"{gid}_dev_clear",
        on_click=complete_gate,
        args=(gid, f"{gid}-CLUE"),
    )


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

render = load_renderer(cur)
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
