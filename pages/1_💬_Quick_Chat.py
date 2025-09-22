import asyncio
import streamlit as st

from services import prompts
from ui.components import sidebar
from ui.interactions import chat_handler, book_handler

st.set_page_config(
    page_title="Quick Chat",
    page_icon="💬",
    layout="wide"
)

sidebar.show()

st.header("Quick Chat")
st.write("Get instant answers to your software development and coding questions.")
ask_book = st.checkbox("Ask the Pragmatic Programmer book?", value=False)

# Ensure the session state is initialized
if "messages" not in st.session_state:
    initial_messages = [{"role": "system",
                         "content": prompts.quick_chat_system_prompt()}]
    st.session_state.messages = initial_messages

# Print all messages in the session state
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
    avatar = "🔎" if message["role"] == "evidence" else None
    if avatar:
        with st.chat_message(message["role"], avatar=avatar):
            page_number = message["page_number"]
            with st.expander(f"See page {page_number}", expanded=False):
                st.write(message["content"], unsafe_allow_html=True)

    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# React to the user prompt
if prompt := st.chat_input("Ask a software development or coding question..."):
    if ask_book:
        asyncio.run(book_handler.ask_book(st.session_state.messages, prompt))
        st.rerun()
    else:
        asyncio.run(chat_handler.chat(st.session_state.messages, prompt))
        st.rerun()
