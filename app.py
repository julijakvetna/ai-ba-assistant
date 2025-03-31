import streamlit as st
from generator import generate_user_story, generate_user_story_enhanced
from io import BytesIO
from docx import Document
from generator import generate_flowchart
from generator import generate_bpmn
from generator import generate_user_story, generate_user_story_enhanced, generate_action_items, generate_flowchart, generate_bpmn

st.set_page_config(page_title="AI BA Assistant", layout="centered")
st.title("📋 AI Business Analyst Assistant")

mode = st.radio("Select Mode:", [
    "User Story Generation", 
    "Meeting Transcript → Action Items", 
    "Diagram Generation",
"BPMN Diagram Generation"
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

                # Скачать результат
                txt_bytes = BytesIO(action_items.encode("utf-8"))
                st.download_button(
                    label="Download Action Items (.txt)",
                    data=txt_bytes,
                    file_name="action_items.txt",
                    mime="text/plain"
                )

elif mode == "Diagram Generation":
    st.subheader("Generate Flowchart / Diagram")

    with st.form("diagram_form"):
        process_description = st.text_area("Describe the process or user story flow")
        submitted = st.form_submit_button("Generate Diagram")

        if submitted and process_description:
            with st.spinner("Generating diagram..."):
                diagram_code = generate_flowchart(process_description)
                st.success("Diagram Generated:")
                st.code(diagram_code, language="mermaid")

elif mode == "BPMN Diagram Generation":
    st.subheader("Generate BPMN Diagram")

    with st.form("bpmn_form"):
        bpmn_description = st.text_area("Describe the BPMN process (e.g. ':user logs in; :system validates;')")
        submitted = st.form_submit_button("Generate BPMN Diagram")

    if submitted and bpmn_description:
        with st.spinner("Generating BPMN diagram..."):
            bpmn_code, diagram_url = generate_bpmn(bpmn_description)
            st.success("BPMN Diagram Generated!")
            st.code(bpmn_code, language="plantuml")
            st.image(diagram_url, caption="BPMN Diagram (PlantUML Server)")

            # Optional download
            from io import BytesIO
            bpmn_bytes = BytesIO(bpmn_code.encode("utf-8"))
            st.download_button(
                label="⬇️ Download BPMN Diagram (.puml)",
                data=bpmn_bytes,
                file_name="bpmn_diagram.puml",
                mime="text/plain"
            )
