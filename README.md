# 📋 AI Business Analyst Assistant

Welcome to **AI BA Assistant** — your AI-powered helper to speed up Business Analyst tasks.

---

## 🚀 Features

✅ **User Story Generation**
- Generates User Stories with Acceptance Criteria based on business descriptions.
- Optionally adds Non-Functional Acceptance Criteria.

✅ **Meeting Transcript → Action Items**
- Extracts clear action items from meeting transcripts.

✅ **Diagram Generation (Flowchart & BPMN)**
- Converts process descriptions or user stories into:
  - **Flowchart** in Mermaid.js syntax
  - **BPMN Diagram** in PlantUML syntax
- Displays BPMN diagram PlantUML code and provides a link to visualize it using a public PlantUML server.

✅ **Project Context Reminder**
- Allows selecting or adding a project.
- Displays project goals, stakeholders, constraints, and current issues.
- Context information is automatically shown when working with User Stories, Action Items, or Diagrams.
- Project data is stored locally in `project_context.json` and can be updated from the app interface.

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/julijakvetna/ai-ba-assistant.git
cd ai-ba-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Create `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_key_here
```

---

## 🌐 Public Demo

The app is available online via Streamlit Cloud:
**https://your-streamlit-app-link**

---

## 🌟 Diagram Generation Usage

1. Select **Diagram Generation** mode.
2. Describe the process or user story in simple steps, e.g.:

```
User logs into the system -> User views dashboard -> User selects a report -> System generates the report -> User downloads the report
```

3. The app will display:
   - Mermaid.js flowchart code
   - BPMN Diagram code in PlantUML syntax
   - Direct visualization link via public PlantUML server:
     `https://www.plantuml.com/plantuml/uml/{encoded-data}`

---

## 📌 Roadmap (Next Features)

- Export Vision, Scope, Backlog drafts
- SRS and BRD template generation
- Jira & Confluence integration
- Risk analysis for requirements
- User Story Map & Data Flow diagrams
- Multi-project & multi-client support
