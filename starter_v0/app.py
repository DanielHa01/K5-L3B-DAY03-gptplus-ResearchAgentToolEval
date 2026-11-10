from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from chat import run_model_tool_loop
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools


ROOT = Path(__file__).parent
ARTIFACTS = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "events" not in st.session_state:
        st.session_state.events = []


def run_request(prompt: str, provider_name: str, model: str | None, max_rounds: int) -> dict:
    provider = make_provider(provider_name)
    declarations = load_tool_declarations(ARTIFACTS / "tools.yaml")
    tools = to_openai_tools(declarations)
    system_prompt = (ARTIFACTS / "system_prompt.md").read_text(encoding="utf-8")
    messages = [*st.session_state.messages, {"role": "user", "content": prompt}]
    result = run_model_tool_loop(
        provider=provider,
        messages=[{"role": "system", "content": system_prompt}, *messages],
        tools=tools,
        model=model or getattr(provider, "default_model", None),
        max_tool_rounds=max_rounds,
    )
    st.session_state.messages.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": result.get("assistant_text", "")},
    ])
    st.session_state.events.extend(result.get("tool_events", []))
    return result


init_state()

with st.sidebar:
    st.title("🔎 Research Agent")
    provider_name = st.selectbox("Provider", ["openai", "openrouter", "anthropic", "gemini", "ollama"])
    model = st.text_input("Model (optional)", placeholder="Dùng model mặc định")
    max_rounds = st.slider("Max tool rounds", min_value=1, max_value=8, value=4)
    if st.button("Xóa cuộc trò chuyện"):
        st.session_state.messages = []
        st.session_state.events = []
        st.rerun()

st.title("Research Agent")
st.write("Tìm kiếm web, tin tức, bài đăng xã hội, paper và đọc URL bằng tool được khai báo.")

for message in st.session_state.messages:
    if message["content"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Bạn muốn nghiên cứu điều gì?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                result = run_request(prompt, provider_name, model.strip() or None, max_rounds)
                st.markdown(result.get("assistant_text") or "Đã xử lý yêu cầu.")
                if result.get("status") == "waiting_for_user":
                    st.info("Agent đang chờ thông tin hoặc xác nhận tiếp theo.")
            except Exception as exc:
                st.error(f"Không thể chạy agent: {type(exc).__name__}: {exc}")

if st.session_state.events:
    with st.expander("Tool activity", expanded=False):
        for index, event in enumerate(st.session_state.events, start=1):
            st.markdown(f"**{index}. {event.get('tool', 'unknown')}**")
            st.json(event)
