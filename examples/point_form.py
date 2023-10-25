import requests
from gbnf_compiler.compiler import GBNFCompiler
from gbnf_compiler.rules import *


template = "I might need the following supplementary information:\n1. {{d1}}2. {{d2}}3. {{d3}}4. {{d4}}5. {{d5}}"

# We should use Single Line in here for simple point-form instead of Item Rule to make this more reasonable.
c = GBNFCompiler(template, { 'd1': SingleLine(), 'd2': SingleLine(), 'd3': SingleLine(), 'd4': SingleLine(), 'd5': SingleLine() })

def template(role: str, prompt: str):
    return """[INST] <<SYS>>
{role}
<</SYS>>
{prompt}
[/INST]""".format(role=role, prompt=prompt)

role = "You are a market researcher, your goal is to help the project manager to finish relevant tasks with your expertise."
prompt = "If the objective is to create a market research report on pet snack market, what supplementary information about the objective will you need from the boss to start the research?"



data_json = { "prompt": template(role, prompt), "temperature": 0.0, "n_predict": 512, "top_p": 0.2, "top_k": 10, "stream": False, 'grammar': c.grammar() }

resp = requests.post(
    url="http://127.0.0.1:9999/completion",
    headers={"Content-Type": "application/json"},
    json=data_json,
)
result = resp.json()["content"]

print(f"Prompt: {prompt}")
print(result)
print(c.parse(result))