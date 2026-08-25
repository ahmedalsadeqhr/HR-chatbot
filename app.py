import base64
import os

import streamlit as st

from groq_client import GroqAPIError, get_text_response, get_vision_response
from knowledge_base import build_system_prompt
from salary_calculator import (
    extract_salary_amount,
    is_no_commission,
    is_salary_calc_request,
    salary_calc_context,
)
from styles import render_styles
from translations import UI

st.set_page_config(
    page_title="مساعد HR - 51Talk Egypt",
    page_icon="🐣",
    layout="centered",
)


def _load_toki() -> str:
    path = os.path.join(os.path.dirname(__file__), "toki.png")
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


TOKI_B64 = _load_toki()

# ── Language state (must be before any UI rendering) ─────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
lang = st.session_state.lang
T = UI[lang]

render_styles(lang)

# ── Star field (decorative, fixed background) ────────────────────────────────
st.markdown("""
<div class="star-field" aria-hidden="true">
  <div class="stars-sm"></div>
  <div class="stars-md"></div>
  <div class="stars-lg"></div>
</div>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
_toki_src = f"data:image/png;base64,{TOKI_B64}" if TOKI_B64 else "https://placehold.co/90x90/FFC800/162040?text=HR"
st.markdown(f"""
<div class="chat-header">
    <div class="toki-wrap">
        <img src="{_toki_src}" alt="Toki">
    </div>
    <div><span class="brand-badge">51Talk Egypt</span></div>
    <h1>{T["header_title"]}</h1>
    <p>{T["header_sub"]}</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <img src="{_toki_src}" alt="Toki">
        <div>
            <div class="sb-text">51Talk Egypt</div>
            <div class="sb-sub">{T["brand_sub"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(T["switch_lang"], use_container_width=True, key="lang_toggle"):
        st.session_state.lang = "en" if lang == "ar" else "ar"
        st.session_state.messages = []
        st.session_state.pending_salary_gross = None
        st.session_state.consumed_upload_id = st.session_state.get("attached_upload_id")
        st.session_state.attached_image = None
        st.rerun()

    st.markdown(f'<p class="sidebar-title" style="margin-top:0.8rem">{T["section_policies"]}</p>', unsafe_allow_html=True)
    for s in T["suggestions"]:
        if st.button(s, use_container_width=True, key=s):
            st.session_state["pending_input"] = s

    st.markdown(f'<p class="sidebar-title" style="margin-top:1rem">{T["section_italent"]}</p>', unsafe_allow_html=True)
    for s in T["italent_suggestions"]:
        if st.button(s, use_container_width=True, key=s):
            st.session_state["pending_input"] = s

    st.markdown(f"""
    <div class="hr-card">
        <div class="label">{T["hr_label"]}</div>
        <div class="email">hr.egy@51talk.com</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(T["clear_chat"], use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_salary_gross = None
        st.session_state.consumed_upload_id = st.session_state.get("attached_upload_id")
        st.session_state.attached_image = None
        st.rerun()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "attached_image" not in st.session_state:
    st.session_state.attached_image = None
if "attached_upload_id" not in st.session_state:
    st.session_state.attached_upload_id = None
if "consumed_upload_id" not in st.session_state:
    st.session_state.consumed_upload_id = None
if "pending_salary_gross" not in st.session_state:
    st.session_state.pending_salary_gross = None

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(T["welcome"])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image_b64"):
            st.image(base64.b64decode(msg["image_b64"]), width=260)
        st.markdown(msg["content"])


# ── API call helpers ──────────────────────────────────────────────────────────
def _error_message(code: str) -> str:
    mapping = {
        "missing_key":  T["api_error"],
        "invalid_key":  T["api_invalid_key"],
        "rate_limit":   T["api_rate_limit"],
        "connection":   T["api_connection"],
    }
    return mapping.get(code, T["api_generic"])


def _call_text(messages_for_api: list[dict]) -> str | None:
    try:
        return get_text_response(messages_for_api, build_system_prompt(lang))
    except GroqAPIError as exc:
        st.error(_error_message(str(exc)))
        return None


def _call_vision(question: str, image_b64: str, mime: str) -> str | None:
    try:
        return get_vision_response(question, image_b64, mime, T["vision_system"], T["vision_default_q"])
    except GroqAPIError as exc:
        st.error(_error_message(str(exc)))
        return None


# ── Input handling ────────────────────────────────────────────────────────────
def _record_and_show_user(user_input: str, image_data: tuple | None) -> None:
    image_b64 = base64.b64encode(image_data[0]).decode() if image_data else None
    msg_record: dict = {"role": "user", "content": user_input}
    if image_b64:
        msg_record["image_b64"] = image_b64
    st.session_state.messages.append(msg_record)
    with st.chat_message("user"):
        if image_data:
            st.image(image_data[0], width=260)
        st.markdown(user_input)


def _clear_attached_image() -> None:
    st.session_state.consumed_upload_id = st.session_state.attached_upload_id
    st.session_state.attached_image = None


def _show_assistant(reply: str) -> None:
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    _clear_attached_image()


def _call_and_show_assistant(effective_input: str, messages_for_api: list[dict] | None = None) -> None:
    if messages_for_api is None:
        messages_for_api = st.session_state.messages[:-1] + [
            {"role": "user", "content": effective_input}
        ]
    with st.chat_message("assistant"):
        with st.spinner(T["spinner"]):
            reply = _call_text(messages_for_api)
        if reply:
            st.markdown(reply)
    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
    _clear_attached_image()


def handle_input(user_input: str) -> None:
    image_data = st.session_state.attached_image
    image_b64 = base64.b64encode(image_data[0]).decode() if image_data else None
    pending_gross = st.session_state.pending_salary_gross

    # ── Commission follow-up ──────────────────────────────────────────────────
    if not image_data and pending_gross is not None:
        commission = extract_salary_amount(user_input)
        no_comm = is_no_commission(user_input)

        if commission is not None or no_comm:
            comm_amount = commission or 0.0
            total = pending_gross + comm_amount
            st.session_state.pending_salary_gross = None

            if comm_amount > 0:
                calc_note = T["calc_with_comm"].format(base=pending_gross, comm=comm_amount, total=total)
            else:
                calc_note = T["calc_no_comm"].format(base=pending_gross)

            try:
                effective_input = (
                    user_input
                    + f"\n\n[{calc_note}]\n\n"
                    + salary_calc_context(total)
                )
            except ValueError:
                _record_and_show_user(user_input, image_data)
                with st.chat_message("assistant"):
                    st.markdown(T["calc_out_of_range"])
                st.session_state.messages.append({"role": "assistant", "content": T["calc_out_of_range"]})
                return

            _record_and_show_user(user_input, image_data)
            _call_and_show_assistant(effective_input)
            return

        _record_and_show_user(user_input, image_data)
        _call_and_show_assistant(user_input, st.session_state.messages[:])
        return

    # ── Salary calculation request ────────────────────────────────────────────
    if not image_data and is_salary_calc_request(user_input):
        gross = extract_salary_amount(user_input)
        if gross:
            st.session_state.pending_salary_gross = gross
            _record_and_show_user(user_input, image_data)
            reply = T["commission_q"].format(gross=gross)
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            return

    # ── Default: LLM Q&A ─────────────────────────────────────────────────────
    _record_and_show_user(user_input, image_data)
    messages_for_api = st.session_state.messages[:]

    with st.chat_message("assistant"):
        with st.spinner(T["spinner"]):
            if image_data:
                reply = _call_vision(user_input, image_b64, image_data[1])
            else:
                reply = _call_text(messages_for_api)
        if reply:
            st.markdown(reply)

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
    _clear_attached_image()


# ── Payslip upload zone ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="upload-zone">
    <div class="uz-title">{T["upload_title"]}</div>
    <div class="uz-hint">{T["upload_hint"]}</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    label="",
    type=["png", "jpg", "jpeg", "webp"],
    label_visibility="collapsed",
    key="payslip_upload",
)

if uploaded and uploaded.file_id == st.session_state.consumed_upload_id:
    # Streamlit keeps returning the same file across reruns until the user
    # removes it from the widget; skip re-attaching one we've already sent.
    uploaded = None

if uploaded:
    img_bytes = uploaded.read()
    mime = uploaded.type or "image/jpeg"
    st.session_state.attached_image = (img_bytes, mime)
    st.session_state.attached_upload_id = uploaded.file_id
    st.image(img_bytes, caption=T["image_caption"], width=260)
elif st.session_state.attached_image:
    st.markdown(f'<span class="attached-badge">{T["attached_badge"]}</span>', unsafe_allow_html=True)

if "pending_input" in st.session_state:
    pending = st.session_state.pop("pending_input")
    handle_input(pending)

placeholder = T["placeholder_img"] if st.session_state.attached_image else T["placeholder"]
if prompt := st.chat_input(placeholder):
    handle_input(prompt)
