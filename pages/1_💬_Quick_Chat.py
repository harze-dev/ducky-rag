import asyncio
import io
import streamlit as st
from PIL import Image

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
                # st.caption(f"Page {page_number}")
                if evidence["page_image_data"]:
                    display_width = 600
                    page_image = Image.open(io.BytesIO(evidence["page_image_data"]))
                    if page_image.width > display_width:
                        ratio = display_width / float(page_image.width)
                        new_height = int(page_image.height * ratio)
                        page_image = page_image.resize((display_width, new_height), Image.Resampling.LANCZOS)
                    st.image(
                        page_image,
                        width='content',
                    )
                    st.download_button(
                        label="Download page",
                        data=evidence["page_image_data"],
                        file_name=f"pragmatic_programmer_page_{page_number}.png",
                        mime="image/png",
                        key=f"download_page_{page_number}",
                    )
                else:
                    st.info("The page image could not be rendered.")

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
