import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")

PROMPT = """
Generate ONE detailed manual test case of type: {tc_type}

User Story:
{story}

URL:
{url}

Return STRICT JSON:
{{
  "id": "",
  "title": "",
  "type": "",
  "priority": "",
  "preconditions": "",
  "steps": [],
  "expected_result": ""
}}
"""

def generate_test_case(story, url, tc_type):
    prompt = PROMPT.format(story=story, url=url, tc_type=tc_type)

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        max_tokens=1200,
        temperature=0.2
    )

    txt = res.choices[0].message.content
    cleaned = txt.replace("```json","").replace("```","").strip()
    return json.loads(cleaned)
