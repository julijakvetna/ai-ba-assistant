import streamlit as st
from generator import generate_user_story, generate_user_story_enhanced
from io import BytesIO
from docx import Document
from generator import generate_flowchart

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
        bpmn_description = st.text_area("Describe the business process (for BPMN)")
        submitted = st.form_submit_button("Generate BPMN Diagram")

        if submitted and bpmn_description:
            with st.spinner("Generating BPMN diagram..."):
                bpmn_code = generate_bpmn(bpmn_description)
                st.success("BPMN Diagram Code:")
                st.code(bpmn_code, language="plantuml")

                # Embed PlantUML live render
                encoded = bpmn_code.replace("@startuml", "").replace("@enduml", "")
                encoded = encoded.replace(" ", "%20").replace("\n", "%0A")
                plantuml_url = f"https://www.plantuml.com/plantuml/svg/~h{encoded}"
                st.markdown(f"![BPMN Diagram]({plantuml_url})")

                # Download as .puml
                puml_bytes = BytesIO(bpmn_code.encode("utf-8"))
                st.download_button(
                    label="⬇️ Download BPMN (.puml)",
                    data=puml_bytes,
                    file_name="bpmn_diagram.puml",
                    mime="text/plain"
                )

