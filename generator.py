import os
from openai import OpenAI
from dotenv import load_dotenv

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

