import streamlit as st
import json
import os
from generator import (
    generate_user_story,
    generate_user_story_enhanced,
    generate_action_items,
    generate_diagram
)
from io import BytesIO
from docx import Document

# File to store project context
PROJECT_FILE = "project_context.json"

# Load or initialize project data
if os.path.exists(PROJECT_FILE):
    with open(PROJECT_FILE, "r") as f:
        project_data = json.load(f)
else:
    project_data = {}

st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("\ud83d\udccb AI Business Analyst Assistant")

mode = st.radio("Select Mode:", [
    "User Story Generation",
    "Meeting Transcript \u2794 Action Items",
    "Diagram Generation"
])

# Project Selection
selected_project = st.selectbox("Select Project:", list(project_data.keys()) + ["+ Add New Project"])

if selected_project == "+ Add New Project":
    with st.form("new_project_form"):
        new_name = st.text_input("Project Name")
        goals = st.text_input("Goals")
        stakeholders = st.text_input("Stakeholders")
        constraints = st.text_input("Constraints")
        issues = st.text_input("Current Issues")
        submitted = st.form_submit_button("Add Project")

    if submitted and new_name:
        project_data[new_name] = {
            "goals": goals,
            "stakeholders": stakeholders,
            "constraints": constraints,
            "issues": issues
        }
        with open(PROJECT_FILE, "w") as f:
            json.dump(project_data, f, indent=2)
        st.experimental_rerun()

if selected_project in project_data:
    context = project_data[selected_project]
    st.markdown(f"""
        <div style='background-color:#f0f4ff;padding:10px;border-radius:5px;'>
            <b>\ud83c\udfaf Goals:</b> {context['goals']}  
            <b>\ud83d\udc65 Stakeholders:</b> {context['stakeholders']}  
            <b>\ud83d\udd27 Constraints:</b> {context['constraints']}  
            <b>\u2757\ufe0f Current Issues:</b> {context['issues']}
        </div>
    """, unsafe_allow_html=True)

# --- Modes ---

if mode == "User Story Generation":
    st.subheader("Generate User Story with Acceptance Criteria")

    enhanced = st.checkbox("Add Non-Functional Acceptance Criteria")

    with st.form("user_story_form"):
        description = st.text_area("Describe a feature, business need, or client request")
        submitted = st.form_submit_button("Generate User Story")

    if submitted and description:
        if enhanced:
            user_story = generate_user_story_enhanced(description)
        else:
            user_story = generate_user_story(description)

        st.subheader("Generated User Story")
        st.code(user_story)

        # Save as .docx
        doc = Document()
        doc.add_paragraph(user_story)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="\ud83d\udd39 Download User Story (.docx)",
            data=buffer,
            file_name="user_story.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

elif mode == "Meeting Transcript \u2794 Action Items":
    st.subheader("Extract Action Items from Meeting Transcript")

    with st.form("transcript_form"):
        transcript = st.text_area("Paste meeting transcript here")
        submitted = st.form_submit_button("Extract Action Items")

    if submitted and transcript:
        with st.spinner("Analyzing transcript..."):
            action_items = generate_action_items(transcript)
        st.success("Action Items extracted:")
        st.write(action_items)

        # Download action items
        txt_bytes = BytesIO(action_items.encode("utf-8"))
        st.download_button(
            label="Download Action Items (.txt)",
            data=txt_bytes,
            file_name="action_items.txt",
            mime="text/plain"
        )

elif mode == "Diagram Generation":
    st.subheader("Generate Flowchart / BPMN Diagram")

    with st.form("diagram_form"):
        process_description = st.text_area("Describe the process or user story flow")
        submitted = st.form_submit_button("Generate Diagram")

    if submitted and process_description:
        with st.spinner("Generating diagram..."):
            mermaid_code, bpmn_code, bpmn_link = generate_diagram(process_description)

        st.success("Flowchart Code:")
        st.code(mermaid_code, language="mermaid")

        st.success("BPMN Diagram Code:")
        st.code(bpmn_code, language="plantuml")

        st.markdown(f"**BPMN Diagram (PlantUML Server):** [View Diagram]({bpmn_link})")

