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
                        "page_pdf_data": None
                    }

                # c. Extract returned values
                answer = rag_result["answer"]
                context = rag_result["context"]
                page_number = rag_result["page_number"]
                page_pdf_data = rag_result["page_pdf_data"]

        # d. Clear spinner
        spinner_placeholder.empty()

        # 4. Display response
        # a. Show answer
        st.write(f"{answer}")

        # b. Create evidence section only when a page image is available
        evidence = {
            "page_number": page_number,
            "context": context,
            "page_pdf_data": page_pdf_data,
        }

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
