import streamlit as st
import services.rag

async def ask_book(messages, prompt):
    """
    Handles the UI flow for asking questions about "The Pragmatic Programmer" book,
    including displaying user messages, processing RAG responses, and updating the chat history.

    Args:
        messages: List of message dictionaries with conversation history
        prompt: The user's question about the book

    Returns:
        Updated messages list with the new conversation
    """
    # Add the user's message to the conversation history
    messages.append({"role": "user", "content": prompt})

    # 1. Display user's prompt in chat UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Create placeholder for spinner
    spinner_placeholder = st.empty()

    # 3. Inside assistant chat message
    with st.chat_message("assistant"):
        # a. Show loading spinner
        with spinner_placeholder:
            with st.spinner("Asking the Pragmatic Programmer book..."):
                # b. Call RAG service
                rag_result = await services.rag.ask_book(prompt, return_image=True)
                if rag_result is None:
                    rag_result = {
                        "answer": ":red[There was an error using retrieval augmented generation. Have you implemented the services.rag functionality?]",
                        "context": "",
                        "page_number": "N/A",
                        "image_data": None
                    }

                # c. Extract returned values
                answer = rag_result["answer"]
                context = rag_result["context"]
                page_number = rag_result["page_number"]
                image_data = rag_result["image_data"]

        # d. Clear spinner
        spinner_placeholder.empty()

        # 4. Display response
        # a. Show answer
        st.write(f"{answer}")

        # b. Handle image data
        if image_data:
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_html = f'<img src="data:image/png;base64,{image_base64}" style="max-width: 100%;">'
        else:
            image_html = "No image available."

        # 5. Create evidence section
        evidence = f"""
        <div style="color: gray; font-size: 10pt;">Page Number: {page_number}</div>
        {image_html}
        """

        # 6. Update chat history
        # a. Append answer to messages
        messages.append({"role": "assistant", "content": answer})

        # b. Append evidence to messages
        messages.append({
            "role": "evidence",
            "content": evidence,
            "page_number": page_number
        })

        # c. Update session state
        st.session_state.messages = messages

    # 7. Return messages
    return messages
