import streamlit as st
from generator import generate_user_story, generate_user_story_enhanced, generate_action_items
from io import BytesIO
from docx import Document

st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("📋 AI Business Analyst Assistant")

mode = st.radio("Select Mode:", ["User Story Generation", "Meeting Transcript → Action Items"])

if mode == "User Story Generation":
    st.subheader("Generate User Story with Acceptance Criteria")

    enhanced = st.checkbox("Add Non-Functional Acceptance Criteria")

    with st.form("user_story_form"):
        description = st.text_area("Describe a feature, business need, or client request", height=200)
        submitted = st.form_submit_button("Generate User Story")

        if submitted:
            if not description.strip():
                st.warning("Please enter a description.")
            else:
                with st.spinner("Generating user story..."):
                    if enhanced:
                        result = generate_user_story_enhanced(description)
                    else:
                        result = generate_user_story(description)
                st.success("Done!")
                st.text_area("📄 Generated User Story", result, height=400)

                # Export buttons
                st.download_button(
                    label="💾 Download as .md",
                    data=result.encode('utf-8'),
                    file_name="user_story.md",
                    mime="text/markdown"
                )

                # Export to docx
                doc = Document()
                doc.add_paragraph(result)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button(
                    label="💾 Download as .docx",
                    data=buffer.getvalue(),
                    file_name="user_story.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

if mode == "Meeting Transcript → Action Items":
    st.subheader("Convert Meeting Transcript to Action Items")

    with st.form("transcript_form"):
        transcript = st.text_area("Paste the meeting transcript here", height=200)
        submitted_transcript = st.form_submit_button("Generate Action Items")

        if submitted_transcript:
            if not transcript.strip():
                st.warning("Please enter the transcript.")
            else:
                with st.spinner("Extracting action items..."):
                    result = generate_action_items(transcript)
                st.success("Done!")
                st.text_area("✅ Action Items", result, height=300)

                # Export buttons
                st.download_button(
                    label="💾 Download as .md",
                    data=result.encode('utf-8'),
                    file_name="action_items.md",
                    mime="text/markdown"
                )

                doc = Document()
                doc.add_paragraph(result)
                buffer = BytesIO()
                doc.save(buffer)
                st.download_button(
                    label="💾 Download as .docx",
                    data=buffer.getvalue(),
                    file_name="action_items.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

