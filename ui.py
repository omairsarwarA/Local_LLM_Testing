import streamlit as st

from llm_service import LocalLLM

st.set_page_config(page_title="Local LLM UI", layout="wide")

st.title("💻 Create Test Cases")

# Initialize LLM
llm = LocalLLM("gemma3:1b")

# Text Input
user_input = st.text_area("Enter your query:", height=150)

if st.button("Generate Response"):
    if user_input.strip() == "":
        st.warning("Please enter a query first.")
    else:
        st.info("⏳ Generating response, please wait...")
        response = llm.ask(user_input)
        st.success("Response:")
        st.write(response)
