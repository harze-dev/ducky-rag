import asyncio
import base64
import streamlit as st
import streamlit.components.v1 as components

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
            evidence = message["content"]
            page_number = evidence["page_number"]
            with st.expander(f"See page {page_number}", expanded=False):
                st.caption("Relevant page from the textbook")
                st.write(evidence["context"])
                if evidence["page_pdf_data"]:
                    pdf_base64 = base64.b64encode(evidence["page_pdf_data"]).decode("utf-8")
                    pdf_embed = f"""
                        <iframe
                            src="data:application/pdf;base64,{pdf_base64}"
                            width="100%"
                            height="900"
                            style="border: 1px solid #ddd; border-radius: 8px;"
                        ></iframe>
                    """
                    components.html(pdf_embed, height=920, scrolling=True)

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
