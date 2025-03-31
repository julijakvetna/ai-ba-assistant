import streamlit as st
from generator import generate_user_story, generate_user_story_enhanced, generate_action_items, generate_diagram
from io import BytesIO
from docx import Document

st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("📋 AI Business Analyst Assistant")

mode = st.radio("Select Mode:", [
    "User Story Generation",
    "Meeting Transcript → Action Items",
    "Diagram Generation"
])

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

        # Download
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

        # Download
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

