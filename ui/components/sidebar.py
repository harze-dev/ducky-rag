import streamlit as st


def show() -> None:
    """
    Displays the sidebar with the Ducky logo and a reload button.

    This function creates a consistent sidebar across all pages of the application,
    including the Ducky logo with version number and a reload button that clears
    the session state and reruns the application.

    Returns:
        None
    """
    with st.sidebar:
        st.markdown(f"""
            <a href="/" style="color:black;text-decoration: none;">
                <div style="display:table;margin-left:0%;">
                    <img src="app/static/logo.png" width="80"><span style="color: white">&nbsp;Ducky</span>
                    <span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v2025.09</span>
                </div>
            </a>
            <br>
                """, unsafe_allow_html=True)

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.rerun()
