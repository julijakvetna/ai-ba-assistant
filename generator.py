import os
import base64
import zlib
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- User Story Generation ---
def generate_user_story(description):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Generate a User Story with Acceptance Criteria based on: {description}"}
        ]
    )
    return response.choices[0].message.content.strip()


def generate_user_story_enhanced(description):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Generate a User Story with functional and non-functional Acceptance Criteria based on: {description}"}
        ]
    )
    return response.choices[0].message.content.strip()


# --- Action Items ---
def generate_action_items(transcript):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Extract clear action items from the following meeting transcript: {transcript}"}
        ]
    )
    return response.choices[0].message.content.strip()


# --- Diagram Generation ---
def compress_plantuml(s):
    data = zlib.compress(s.encode('utf-8'))[2:-4]
    return base64.b64encode(data).decode('utf-8')


def generate_diagram(description):
    # Flowchart
    steps = description.split("->")
    mermaid_code = "graph TD\n"
    for i, step in enumerate(steps):
        mermaid_code += f"    step{i}[{step.strip()}]"
        if i < len(steps) - 1:
            mermaid_code += f" --> step{i+1}\n"

    # BPMN PlantUML
    bpmn_code = f"""@startuml
start
{chr(10).join([f":{s.strip()};' step {i+1}" for i, s in enumerate(steps)])}
stop
@enduml"""
    encoded = compress_plantuml(bpmn_code)
    bpmn_link = f"https://www.plantuml.com/plantuml/png/{encoded}"

    return mermaid_code, bpmn_code, bpmn_link

