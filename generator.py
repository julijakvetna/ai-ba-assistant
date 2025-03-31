import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import zlib

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def load_prompt_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_user_story(description):
    prompt = load_prompt_template("prompts/story_prompt.txt").format(description=description)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant for a business analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=800
    )
    return response.choices[0].message.content

def generate_user_story_enhanced(description):
    prompt = load_prompt_template("prompts/story_prompt_enhanced.txt").format(description=description)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant for a business analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content

def generate_action_items(transcript):
    prompt = load_prompt_template("prompts/action_items_prompt.txt").format(transcript=transcript)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant for a business analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content

def generate_diagram(description):
    mermaid_code = f"""
graph LR
{" --> ".join([f"{chr(65+i)}({step.strip()})" for i, step in enumerate(description.split('->'))])}
"""
    bpmn_code = f"""
@startuml
start
{chr(10).join([f":{step.strip()};" for step in description.split('->')])}
stop
@enduml
"""
    # Encode PlantUML
    compressed = zlib.compress(bpmn_code.encode("utf-8"))[2:-4]
    encoded = base64.b64encode(compressed).decode("utf-8")
    plantuml_url = f"https://www.plantuml.com/plantuml/uml/~1{encoded}"

    return mermaid_code.strip(), bpmn_code.strip(), plantuml_url

