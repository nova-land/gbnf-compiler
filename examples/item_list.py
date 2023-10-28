'''
Example request with llama.cpp
'''

import requests
from gbnf_compiler import *

prompt = "Give me 3 objectives as a market researcher."
template = "Objectives: \n {{objectives}}"
c = GBNFCompiler(template, { 'objectives': ItemList() })
print(c.grammar())

text = r'''Objectives: 
 - To understand the market and its trends.
- To identify the target audience.
- To find out the competitors.'''
result = c.parse(text)
print(result)

"""
Result:
{
  'objectives': [
    'To understand the market and its trends.',
    'To identify the target audience.',
    'To find out the competitors.'
  ]
}
"""

def template(role: str, prompt: str):
    return """[INST] <<SYS>>
{role}
<</SYS>>
{prompt}
[/INST]""".format(role=role, prompt=prompt)

data_json = {
    "prompt": template("", prompt), "temperature": 0.0,
    "n_predict": 512, "top_p": 0.2, "top_k": 10,
    "stream": False, "grammar": c.grammar() }

resp = requests.post(
    url="http://127.0.0.1:9999/completion",
    headers={"Content-Type": "application/json"},
    json=data_json,
)
result = resp.json()["content"]

print(f"Prompt: {prompt}")
print(result)
print(c.parse(result))