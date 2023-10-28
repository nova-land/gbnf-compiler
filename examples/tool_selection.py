'''
Example request with llama.cpp
'''

import requests
from gbnf_compiler import GBNFCompiler, MultipleChoice, SingleSentence

prompt = "What tool will you use for calculate 2^5 ?"
template = "I choose {{tool}} because {{reason}}"
text = "I choose calculator because I need to calculate the result of 2^5."
tools = MultipleChoice('tool', ['calculator', 'web-search', 'web-browse'])
c = GBNFCompiler(template, { 'tool': tools, 'reason': SingleSentence() })
print(c.grammar())

result = c.parse(text)
print(result)


"""
# Bad Example of generating wrong answer without reasoning

prompt = "What is the answer of calculating 2 + 5 ?"
template = "{{answer}}"
c = GBNFCompiler(template, { 'answer': NUMBER_RULE })
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