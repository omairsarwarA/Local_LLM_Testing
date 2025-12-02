import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Local LLM Test Case Generator")

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.text_area("Enter your prompt", height=100)
col1, col2 = st.columns(2)
if col1.button("Send"):
    if prompt.strip():
        res = requests.post(f"{API_URL}/chat", params={"prompt": prompt}).json()
        st.session_state.history.append((prompt, res.get("response", "")))
        prompt = ""

if col2.button("Clear"):
    st.session_state.history = []

for q, a in reversed(st.session_state.history):
    st.markdown(f"**Prompt:** {q}")
    st.markdown(f"**LLM Response:** {a}")
    st.markdown("---")

st.markdown("### Export Options")
col3, col4 = st.columns(2)
if col3.button("Export JSON"):
    requests.get(f"{API_URL}/export/json")
    st.success("Exported JSON as chat_history.json")

if col4.button("Export Excel"):
    requests.get(f"{API_URL}/export/excel")
    st.success("Exported Excel as chat_history.xlsx")
