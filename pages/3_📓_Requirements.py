import asyncio

import streamlit as st

from services.prompts import (
    requirements_prompt, system_requirements_prompt,
    engineering_plan_system_prompt, engineering_plan_prompt,
    risk_mitigation_system_prompt, risk_mitigation_prompt
)
from services.requirements import requirements_service
from ui.components import sidebar
from ui.interactions import chat_handler


# Private helper functions
def _display_file_info_and_actions(title_or_filename, content, download_key_prefix, is_filename=True):
    """Display file information and download button in 3-column layout"""
    file_lines = len(content.split('\n'))
    file_chars = len(content)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if is_filename:
            st.caption("**File Name:**")
            st.write(title_or_filename)
        else:
            st.caption("**Document Type:**")
            st.write(title_or_filename)
    with col2:
        st.caption("**File Stats:**")
        st.write(f"{file_lines:,} lines • {file_chars:,} chars")
    with col3:
        st.caption("**Actions:**")
        filename = title_or_filename if is_filename else st.session_state.get('generated_filename', 'document.txt')
        st.download_button(
            label="📥 Download",
            data=content,
            file_name=filename,
            mime="text/plain",
            key=f"{download_key_prefix}_download"
        )


def _display_content(content):
    """Display content with markdown, falling back to code if markdown fails"""
    st.markdown("#### Content:")
    try:
        st.markdown(content)
    except:
        st.code(content, language=None)


def _clear_generation_state():
    """Clear all generation-related session state variables"""
    for key in ['generation_content', 'generation_type', 'generated_filename', 'generation_tab']:
        if key in st.session_state:
            del st.session_state[key]


def _clear_file_selections():
    """Clear all file selection session state variables"""
    for key in ['selected_req_file', 'selected_studio_file']:
        if key in st.session_state:
            del st.session_state[key]


def _clear_generation_state_and_rerun():
    """Clear generation state and trigger rerun"""
    _clear_generation_state()
    st.rerun()

st.set_page_config(
    page_title="Requirements",
    page_icon="📓",
    layout="wide"
)

st.header("Requirements")

sidebar.show()

st.markdown("<br>", unsafe_allow_html=True)

# Create 3-column layout
col1, col2, col3 = st.columns([2, 1, 1])

# Column 1: Requirements generation form
with col1:
    st.subheader("📝 Generate Requirements")

    product_name = st.text_input("What is the name of your product?", placeholder="Enter the name of your product here.")

    product_description = st.text_area("Describe your product.", placeholder="Enter a description of your product here.")

    requirement_type = st.selectbox("What type of requirement document should we generate?",
                                  ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"])

    generate_button = st.button("Generate document&nbsp;&nbsp;➠", type="primary")

    if generate_button:
        if not product_name.strip():
            st.error("Please enter a product name.")
        elif not product_description.strip():
            st.error("Please enter a product description.")
        else:
            # Clear any existing selections when starting new generation
            if 'selected_req_file' in st.session_state:
                del st.session_state['selected_req_file']
            if 'selected_studio_file' in st.session_state:
                del st.session_state['selected_studio_file']

            # Store form values in session state for generation
            st.session_state['product_name'] = product_name
            st.session_state['product_description'] = product_description

            # Set generation state for requirements documents
            st.session_state['generating'] = True
            st.session_state['generation_type'] = requirement_type
            st.session_state['generation_content'] = ''
            st.session_state['generation_tab'] = 'requirements'
            st.rerun()

# Column 2: File browser for requirements documents
with col2:
    st.subheader("📁 Requirements Docs")

    # Get requirements files from requirements service
    requirements_files = requirements_service.list_requirements_files()

    # Requirements Documents Section
    if requirements_files:
        with st.expander(f"📋 Requirements ({len(requirements_files)})", expanded=False):
            # Clear button
            if st.button("❌ Clear Requirements Selection", key="clear_req_btn"):
                if 'selected_req_file' in st.session_state:
                    del st.session_state['selected_req_file']
                st.rerun()

            # Current selection display
            current_req = st.session_state.get('selected_req_file')
            if current_req:
                st.info(f"📋 Selected: {current_req}")

            st.write("**Click to select:**")
            # Individual buttons for each file
            for file in requirements_files:
                is_selected = st.session_state.get('selected_req_file') == file
                button_type = "primary" if is_selected else "secondary"
                if st.button(f"📋 {file}", key=f"req_btn_{file}", type=button_type):
                    st.session_state['selected_req_file'] = file
                    st.rerun()
    else:
        st.info("*No requirement documents yet*")
        # Clear session state if no files exist
        if 'selected_req_file' in st.session_state:
            del st.session_state['selected_req_file']

    if not requirements_files:
        st.write("Generate your first requirement document using the left column!")

    # Management buttons at the bottom
    st.markdown("---")

    # Refresh button
    if st.button("🔄 Refresh File List", help="Refresh the file list to show any new documents"):
        st.rerun()

    # Clear All Files button
    if st.button("🗑️ Clear All Files", type="secondary", help="Delete all requirements and studio documents"):
        success, message = requirements_service.clear_all_files()
        if success:
            # Clear session state
            if 'selected_req_file' in st.session_state:
                del st.session_state['selected_req_file']
            if 'selected_studio_file' in st.session_state:
                del st.session_state['selected_studio_file']
            st.success(message)
            st.rerun()  # Refresh the page to update file lists
        else:
            st.error(message)

# Column 3: Project planning and studio documents
with col3:
    st.subheader("🎬 Studio Plans")

    # Get studio files from requirements service
    studio_files = requirements_service.list_studio_files()

    # Studio Documents Section
    if studio_files:
        with st.expander(f"Studio Plans ({len(studio_files)})", expanded=False):
            # Clear button
            if st.button("❌ Clear Studio Selection", key="clear_studio_btn"):
                if 'selected_studio_file' in st.session_state:
                    del st.session_state['selected_studio_file']
                st.rerun()

            # Current selection display
            current_studio = st.session_state.get('selected_studio_file')
            if current_studio:
                st.info(f"🎬 Selected: {current_studio}")

            st.write("**Click to select:**")
            # Individual buttons for each file
            for file in studio_files:
                is_selected = st.session_state.get('selected_studio_file') == file
                button_type = "primary" if is_selected else "secondary"
                if st.button(f"🎬 {file}", key=f"studio_btn_{file}", type=button_type):
                    st.session_state['selected_studio_file'] = file
                    st.rerun()
    else:
        st.info("*No studio documents yet*")
        # Clear session state if no files exist
        if 'selected_studio_file' in st.session_state:
            del st.session_state['selected_studio_file']

    st.markdown("---")

    # Count requirements documents
    num_docs = len(requirements_files) if requirements_files else 0

    if num_docs >= 3:
        st.write(f"**{num_docs} requirements documents available**")
        st.write("Ready to generate project plans!")

        # Generation buttons with less vertical space
        col3a, col3b = st.columns(2)

        with col3a:
            # Engineering Project Plan button
            if st.button("📋 Generate\nEngineering\nProject Plan", type="secondary", key="eng_plan_btn"):
                # Clear any existing selections when starting new generation
                if 'selected_req_file' in st.session_state:
                    del st.session_state['selected_req_file']
                if 'selected_studio_file' in st.session_state:
                    del st.session_state['selected_studio_file']

                # Set generation state for studio documents
                st.session_state['generating'] = True
                st.session_state['generation_type'] = 'Engineering Project Plan'
                st.session_state['generation_content'] = ''
                st.session_state['generation_tab'] = 'studio'
                st.rerun()

        with col3b:
            # Risk Mitigation Plan button
            if st.button("⚠️ Generate\nRisk Mitigation\nPlan", type="secondary", key="risk_plan_btn"):
                # Clear any existing selections when starting new generation
                if 'selected_req_file' in st.session_state:
                    del st.session_state['selected_req_file']
                if 'selected_studio_file' in st.session_state:
                    del st.session_state['selected_studio_file']

                # Set generation state for studio documents
                st.session_state['generating'] = True
                st.session_state['generation_type'] = 'Risk Mitigation Plan'
                st.session_state['generation_content'] = ''
                st.session_state['generation_tab'] = 'studio'
                st.rerun()

    else:
        needed = 3 - num_docs
        st.write(f"**{num_docs} of 3 documents**")
        st.write(f"Need {needed} more requirement document(s) to generate project plans.")

        # Disabled buttons in compact layout
        col3a, col3b = st.columns(2)

        with col3a:
            st.button("📋 Generate\nEngineering\nProject Plan", disabled=True, help="Generate 3+ requirements documents first", key="eng_plan_disabled")

        with col3b:
            st.button("⚠️ Generate\nRisk Mitigation\nPlan", disabled=True, help="Generate 3+ requirements documents first", key="risk_plan_disabled")

# Unified Content Display Area with Permanent Tabs
st.markdown("---")

# Get session state variables
generated_content = st.session_state.get('generation_content')
generation_type = st.session_state.get('generation_type')
generated_filename = st.session_state.get('generated_filename')
generating = st.session_state.get('generating', False)
generation_tab = st.session_state.get('generation_tab', 'requirements')

# Check selected files
selected_req = st.session_state.get('selected_req_file')
selected_studio = st.session_state.get('selected_studio_file')

# Always show tabs
tab1, tab2 = st.tabs(["📋 Requirements Documents", "🎬 Studio Plans"])

with tab1:
    # Requirements Documents Tab Content
    if generating and generation_tab == 'requirements':
        # Show generation in progress for requirements documents
        st.markdown(f"#### 🚀 Generating {generation_type}...")

        # Setup messages for requirements document generation
        messages = []
        system_requirements_prompt_text = system_requirements_prompt(
            st.session_state.get('product_name', 'Product'),
            st.session_state.get('product_description', 'Description')
        )
        messages.append({"role": "system", "content": system_requirements_prompt_text})

        prompt = requirements_prompt(st.session_state.get('product_name', 'Product'), generation_type)
        messages.append({"role": "user", "content": prompt})

        # Create streaming placeholder
        streaming_placeholder = st.empty()
        spinner_placeholder = st.empty()

        with spinner_placeholder:
            with st.spinner(f"Generating {generation_type.lower()}..."):
                try:
                    messages, full_response = asyncio.run(chat_handler.run_conversation(messages, streaming_placeholder))

                    # Save the generated document using requirements service
                    if full_response:
                        success, result = requirements_service.save_requirements_document(
                            full_response, st.session_state.get('product_name', 'Product'), generation_type
                        )

                        if success:
                            st.success(f"✅ Document saved as: {result}")
                            # Set the generated content and clear generation state
                            st.session_state['generation_content'] = full_response
                            st.session_state['generated_filename'] = result
                            st.session_state['generation_type'] = generation_type
                        else:
                            st.error(f"Error saving document: {result}")

                except Exception as e:
                    st.error(f"Error generating document: {str(e)}")

        # Clear generation state and streaming placeholders
        st.session_state['generating'] = False
        streaming_placeholder.empty()
        spinner_placeholder.empty()
        st.rerun()

    elif generated_content and generation_tab == 'requirements':
        # Show generated requirements document
        _display_file_info_and_actions(generation_type, generated_content, "generated_requirements", is_filename=False)

        # Clear generated content button
        if st.button("❌ Clear Generated Content", help="Clear the generated content to view files", key="clear_requirements"):
            _clear_generation_state_and_rerun()

        # Display content
        _display_content(generated_content)

    elif selected_req:
        # Show selected requirements document
        content = requirements_service.read_file_content(selected_req, is_studio_file=False)
        if content:
            _display_file_info_and_actions(f"📋 {selected_req}", content, f"requirements_{selected_req}")
            _display_content(content)
        else:
            st.error(f"❌ Cannot read file: {selected_req}")
    else:
        # Empty state for requirements tab
        st.info("📋 Select a requirements document from the center column or generate a new one using the left column.")

with tab2:
    # Studio Plans Tab Content
    if generating and generation_tab == 'studio':
        # Show generation in progress for studio documents
        st.markdown(f"#### 🚀 Generating {generation_type}...")

        # Get all requirements content using requirements service
        all_requirements, product_name_extracted = requirements_service.get_all_requirements_content()
        num_docs = len(requirements_service.list_requirements_files()) if requirements_service.list_requirements_files() else 0

        # Setup messages based on generation type
        messages = []
        if generation_type == 'Engineering Project Plan':
            system_prompt = engineering_plan_system_prompt(product_name_extracted)
            user_prompt = engineering_plan_prompt(product_name_extracted, all_requirements)
        else:  # Risk Mitigation Plan
            system_prompt = risk_mitigation_system_prompt(product_name_extracted)
            user_prompt = risk_mitigation_prompt(product_name_extracted, all_requirements)

        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        # Create streaming placeholder
        streaming_placeholder = st.empty()
        spinner_placeholder = st.empty()

        with spinner_placeholder:
            with st.spinner(f"Analyzing requirements and creating {generation_type.lower()}..."):
                try:
                    messages, full_response = asyncio.run(chat_handler.run_conversation(messages, streaming_placeholder, max_tokens=50000))

                    # Save the generated plan using requirements service
                    if full_response:
                        plan_type = "Engineering_Project_Plan" if generation_type == 'Engineering Project Plan' else "Risk_Mitigation_Plan"
                        success, result = requirements_service.save_project_plan(
                            full_response, product_name_extracted, plan_type, num_docs
                        )

                        if success:
                            st.success(f"✅ {generation_type} saved to studio: {result}")
                            # Set the generated content and clear generation state
                            st.session_state['generation_content'] = full_response
                            st.session_state['generated_filename'] = result
                            st.session_state['generation_type'] = generation_type
                        else:
                            st.error(f"Error saving plan: {result}")

                except Exception as e:
                    st.error(f"Error generating {generation_type.lower()}: {str(e)}")

        # Clear generation state and streaming placeholders
        st.session_state['generating'] = False
        streaming_placeholder.empty()
        spinner_placeholder.empty()
        st.rerun()

    elif generated_content and generation_tab == 'studio':
        # Show generated studio document
        _display_file_info_and_actions(generation_type, generated_content, "generated_studio", is_filename=False)

        # Clear generated content button
        if st.button("❌ Clear Generated Content", help="Clear the generated content to view files", key="clear_studio"):
            _clear_generation_state_and_rerun()

        # Display content
        _display_content(generated_content)

    elif selected_studio:
        # Show selected studio document
        content = requirements_service.read_file_content(selected_studio, is_studio_file=True)
        if content:
            _display_file_info_and_actions(f"🎬 {selected_studio}", content, f"studio_{selected_studio}")
            _display_content(content)
        else:
            st.error(f"❌ Cannot read file: {selected_studio}")
    else:
        # Empty state for studio tab
        st.info("🎬 Select a studio document from the right sidebar or generate one using the right column (requires 3+ requirements documents).")
