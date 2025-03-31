import os
from openai import OpenAI
from plantuml_encoder import encode_plantuml
from dotenv import load_dotenv
import zlib
import base64

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def load_prompt_template(path="prompts/story_prompt.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_user_story(description):
    prompt = load_prompt_template().format(description=description)

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

def generate_action_items(transcript):
    path = "prompts/action_items_prompt.txt"
    with open(path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(transcript=transcript)

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

def generate_user_story_enhanced(description):
    path = "prompts/story_prompt_enhanced.txt"
    with open(path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(description=description)

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

def generate_flowchart(description):
    prompt = f"""
    Based on the following process description, generate a simple Mermaid.js flowchart:
    
    {description}
    
    Output only the Mermaid diagram code without explanation.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def deflate_and_encode(plantuml_text):
    compressed = zlib.compress(plantuml_text.encode('utf-8'))
    compressed = compressed[2:-4]
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded


def generate_bpmn(bpmn_description):
    bpmn_code = f"""@startuml
{bpmn_description}
@enduml
"""
    encoded = encode_plantuml(bpmn_code)
    diagram_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    return bpmn_code, diagram_url

