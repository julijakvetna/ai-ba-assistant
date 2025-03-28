# ai-ba-assistant
BA Assistant MVP
=======
AI Business Analyst Assistant

This is an internal MVP of a lightweight AI Assistant to help Business Analysts (BAs) in a service IT company working with large clients.

Features:

✏️ User Story Generation (with optional Non-Functional Acceptance Criteria)
📄 Meeting Transcript → Action Items
💾 Export results as .md and .docx
🔄 Simple web interface (Streamlit-based)
🎯 How to Run Locally

Clone the repository (optional):
git clone [repo-url]
cd ai-ba-assistant
Activate virtual environment:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Add your OpenAI API key: Create a .env file:
OPENAI_API_KEY=sk-...
Run the assistant:
python -m streamlit run app.py
🟢 Current MVP Scope

Feature	Status
User Story Generation	✅
Non-Functional Acceptance Criteria Option	✅
Meeting Transcript → Action Items	✅
Export to .md and .docx	✅
🚀 Next Planned Features

Export to Confluence
Jira integration
Project log and context switch helper
Requirements version control

>>>>>>> 74a5849 (MVP ready for testing)
