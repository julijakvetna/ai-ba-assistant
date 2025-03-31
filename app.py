import streamlit as st
from generator import (
    generate_user_story,
    generate_user_story_enhanced,
    generate_action_items,
    generate_diagram,
)
import json
import os

# === Project Context Handling ===
CONTEXT_FILE = "project_context.json"

def load_context():
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_context(context):
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=4)

context = load_context()
current_project = None

# === UI ===
st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("AI Business Analyst Assistant")

mode = st.radio("Select Mode:", [
    "User Story Generation",
    "Meeting Transcript → Action Items",
    "Diagram Generation"
])

# === Project selection ===
st.markdown("### Select Project:")
projects = list(context.keys())
selected = st.selectbox("Select Project:", projects + ["➕ Create new project"])

if selected == "➕ Create new project":
    new_project = st.text_input("Enter new project name:")
    if new_project:
        if new_project not in context:
            context[new_project] = {
                "goals": "",
                "stakeholders": "",
                "constraints": "",
                "issues": ""
            }
            save_context(context)
            st.success(f"Project '{new_project}' created. Please restart the app.")
else:
    current_project = selected

# === Project Context Reminder ===
if current_project:
    project_data = context[current_project]
    with st.expander("📌 Project Context"):
        st.markdown(f"🎯 **Goals**: {project_data.get('goals', 'N/A')}")
        st.markdown(f"👥 **Stakeholders**: {project_data.get('stakeholders', 'N/A')}")
        st.markdown(f"🪝 **Constraints**: {project_data.get('constraints', 'N/A')}")
        st.markdown(f"❗ **Current Issues**: {project_data.get('issues', 'N/A')}")

# === Mode Logic ===
if mode == "User Story Generation":
    st.subheader("Generate User Story with Acceptance Criteria")
    enhanced = st.checkbox("Add Non-Functional Acceptance Criteria")

    with st.form("user_story_form"):
        description = st.text_area("Describe a feature, business need, or client request")
        submitted = st.form_submit_button("Generate User Story")

    if submitted and description:
        user_story = generate_user_story_enhanced(description) if enhanced else generate_user_story(description)
        st.subheader("Generated User Story")
        st.code(user_story, language="markdown")

elif mode == "Meeting Transcript → Action Items":
    st.subheader("Extract Action Items from Meeting Transcript")

    with st.form("transcript_form"):
        transcript = st.text_area("Paste meeting transcript here")
        submitted = st.form_submit_button("Extract Action Items")

    if submitted and transcript:
        with st.spinner("Analyzing transcript..."):
            action_items = generate_action_items(transcript)
        st.success("Action Items extracted:")
        st.write(action_items)

elif mode == "Diagram Generation":
    st.subheader("Generate Flowchart + BPMN Diagram")

    with st.form("diagram_form"):
        description = st.text_area("Describe the process or user story flow")
        submitted = st.form_submit_button("Generate Diagrams")

    if submitted and description:
        with st.spinner("Generating diagrams..."):
            flowchart, bpmn_code, bpmn_link = generate_diagram(description)

        st.success("Flowchart (Mermaid):")
        st.code(flowchart, language="mermaid")

        st.success("BPMN Diagram (PlantUML Syntax):")
        st.code(bpmn_code, language="plantuml")

        st.markdown(f"[🌐 View BPMN Diagram]({bpmn_link})")

