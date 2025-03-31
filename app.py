import streamlit as st
import json
import os
from generator import generate_user_story, generate_user_story_enhanced, generate_action_items, generate_diagram
from io import BytesIO
from docx import Document

PROJECT_FILE = "project_context.json"


def load_project_context():
    if not os.path.exists(PROJECT_FILE):
        return {}
    with open(PROJECT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_project_context(context):
    with open(PROJECT_FILE, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=4)


st.set_page_config(page_title="AI BA Assistant", layout="centered")

st.title("📋 AI Business Analyst Assistant")

mode = st.radio("Select Mode:", [
    "User Story Generation",
    "Meeting Transcript → Action Items",
    "Diagram Generation"
])

# Load Project Context
project_context = load_project_context()
project_names = list(project_context.keys())

selected_project = st.selectbox("Select Project:", project_names + ["➕ Add New Project"])

if selected_project == "➕ Add New Project":
    new_project = st.text_input("Enter new project name")
    if new_project:
        goals = st.text_input("Project Goals")
        stakeholders = st.text_area("Stakeholders (comma separated)")
        constraints = st.text_input("Constraints")
        issues = st.text_area("Current Issues")
        if st.button("Save Project"):
            project_context[new_project] = {
                "goals": goals,
                "stakeholders": [s.strip() for s in stakeholders.split(",")],
                "constraints": constraints,
                "current_issues": issues
            }
            save_project_context(project_context)
            st.success(f"Project '{new_project}' saved. Please reload the page.")
            st.stop()
else:
    st.info(f"""
    **🎯 Goals:** {project_context[selected_project]["goals"]}
    **👥 Stakeholders:** {", ".join(project_context[selected_project]["stakeholders"])}
    **🚧 Constraints:** {project_context[selected_project]["constraints"]}
    **❗️ Current Issues:** {project_context[selected_project]["current_issues"]}
    """)

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

        doc = Document()
        doc.add_paragraph(user_story)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="⬇️ Download User Story (.docx)",
            data=buffer,
            file_name="user_story.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

if mode == "Meeting Transcript → Action Items":
    st.subheader("Extract Action Items from Meeting Transcript")
    with st.form("transcript_form"):
        transcript = st.text_area("Paste meeting transcript here")
        submitted = st.form_submit_button("Extract Action Items")

    if submitted and transcript:
        with st.spinner("Analyzing transcript..."):
            action_items = generate_action_items(transcript)
            st.success("Action Items extracted:")
            st.write(action_items)

        txt_bytes = BytesIO(action_items.encode("utf-8"))
        st.download_button(
            label="Download Action Items (.txt)",
            data=txt_bytes,
            file_name="action_items.txt",
            mime="text/plain"
        )

if mode == "Diagram Generation":
    st.subheader("Generate Flowchart & BPMN Diagram")
    with st.form("diagram_form"):
        process_description = st.text_area("Describe the process or user story flow")
        submitted = st.form_submit_button("Generate Diagram")

    if submitted and process_description:
        with st.spinner("Generating diagrams..."):
            mermaid_code, bpmn_code, plantuml_url = generate_diagram(process_description)
            st.success("Mermaid.js Flowchart Code:")
            st.code(mermaid_code, language="mermaid")

            st.success("BPMN Diagram (PlantUML Syntax):")
            st.code(bpmn_code, language="plantuml")
            st.markdown(f"🌐 [View BPMN Diagram]({plantuml_url})")

