# 📋 AI Business Analyst Assistant

Welcome to **AI BA Assistant** — an AI-powered helper designed to simplify and automate Business Analyst tasks.

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
- Provides PlantUML link for online BPMN visualization.

✅ **Project Context Reminder**
- Allows selecting or adding a project.
- Stores project goals, stakeholders, constraints, and current issues in a local JSON file.
- Displays project context when working with User Stories, Action Items, or Diagrams.

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

## 🌟 Usage

1. Select or create a **Project**.
2. Choose one of the modes:
   - User Story Generation
   - Meeting Transcript → Action Items
   - Diagram Generation
3. Enter the required description or transcript.
4. Receive generated content and download if needed.

---

## 📄 Example project_context.json

```json
{
  "Customer Portal": {
    "goals": "Provide customers access to invoices and support tickets.",
    "stakeholders": "Customer Support, End Users",
    "constraints": "GDPR compliance",
    "issues": "No self-service option for invoices"
  },
  "Timesheet System": {
    "goals": "Track employee working hours and project allocation.",
    "stakeholders": "HR, Employees, Managers",
    "constraints": "Integration with HR system",
    "issues": "Employees often submit timesheets late"
  }
}
```

---

## 📌 Roadmap

- Export Vision, Scope, Backlog drafts
- SRS and BRD template generation
- Jira & Confluence integration
- Risk analysis for requirements
- User Story Map & Data Flow diagrams
- Multi-project & multi-client support

