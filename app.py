import streamlit as st
from generator import generate_user_story, generate_user_story_enhanced
from io import BytesIO
from docx import Document

st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("📋 AI Business Analyst Assistant")

mode = st.radio("Select Mode:", ["User Story Generation", "Meeting Transcript → Action Items"])

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

        # Сохраняем в .docx для загрузки
        doc = Document()
        doc.add_paragraph(user_story)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Добавляем кнопку загрузки
        st.download_button(
            label="📥 Download User Story (.docx)",
            data=buffer,
            file_name="user_story.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

