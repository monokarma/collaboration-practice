"""G3 수상한 강의 공지

G3-A: 여러 공지 중 최신 공식 공지를 고르게 한다.
"""

import streamlit as st

from core import gate_data

GID = "G3"

# 게시 시각은 "YYYY-MM-DD HH:MM" 형식이라 문자열 비교로 순서를 정할 수 있다.
NOTICES = [
    {
        "id": 1,
        "source": "공식",
        "posted": "2026-10-19 09:00",
        "title": "중간고사 대비 특강 안내",
        "body": "특강은 공학관 301호에서 14:00에 시작합니다.",
    },
    {
        "id": 2,
        "source": "비공식",
        "posted": "2026-10-20 08:30",
        "title": "[단톡방] 특강 장소 바뀜!!",
        "body": "도서관 1층으로 15시까지 오래요!",
    },
    {
        "id": 3,
        "source": "공식",
        "posted": "2026-10-20 07:50",
        "title": "[변경] 특강 장소·시간 변경 안내",
        "body": "특강 장소가 공학관 501호로, 시작 시각이 16:30으로 바뀌었습니다. "
                "단톡방에 도는 다른 장소·시간은 사실이 아닙니다.",
    },
    {
        "id": 4,
        "source": "공식",
        "posted": "2026-10-18 17:00",
        "title": "특강 신청 마감 안내",
        "body": "특강 신청은 10월 19일에 마감됩니다.",
    },
]
NOTICE_BY_ID = {n["id"]: n for n in NOTICES}


def latest_official(notices):
    """공식 공지 중 게시 시각이 가장 늦은 공지를 돌려준다."""
    official = [n for n in notices if n["source"] == "공식"]
    return max(official, key=lambda n: n["posted"])


def judge_notice(notice, notices=NOTICES):
    """G3-A: 고른 공지를 판정해 (정답 여부, 안내 문구)를 돌려준다."""
    if notice["id"] == latest_official(notices)["id"]:
        return True, "정답! 이게 최신 공식 공지예요."
    if notice["source"] != "공식":
        return False, "비공식 공지예요. 공식 공지만 믿으세요."
    return False, "공식 공지지만 최신이 아니에요."


def notice_label(notice_id):
    n = NOTICE_BY_ID[notice_id]
    return f"[{n['source']}] {n['posted']}  {n['title']}"


def select_notice():
    """G3-A 화면. 최신 공식 공지를 맞혔으면 그 공지를, 아니면 None을 돌려준다."""
    data = gate_data(GID)
    if "notice_id" in data:
        notice = NOTICE_BY_ID[data["notice_id"]]
        st.success("정답! 이게 최신 공식 공지예요.")
        st.info(notice["body"])
        return notice

    choice = st.radio(
        "최신 공식 공지를 고르세요",
        list(NOTICE_BY_ID),
        index=None,
        format_func=notice_label,
        key=f"{GID}_choice",
    )
    if st.button("공지 선택", key=f"{GID}_select"):
        if choice is None:
            st.warning("공지를 하나 고르세요.")
        else:
            ok, message = judge_notice(NOTICE_BY_ID[choice])
            if ok:
                data["notice_id"] = choice
                st.rerun()
            st.error(message)
    return None


def render():
    select_notice()
