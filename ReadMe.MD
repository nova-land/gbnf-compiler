# GBNF Compiler (Python)

> Dependency-free GBNF Compiler, plug and play for llama.cpp GBNF.

Simple yet powerful GBNF Compiler, use it like handlebars.js with better response from LLMs.

## Why ?

GBNF is very useful to confine the response format from LLMs.

In most of the time, using sentence-based GBNF can produce better result than JSON-based GBNF in most LLMs without fine-tuning, `gbnf-compiler` provides the flexibility to construct or parse sentence / JSON / (anything you can think of) GBNF.

## Getting Started

`pip install gbnf-compiler`

## How to Use

1. Define the LLM Response Template
2. Create the Rule
3. Send it out, done!

```python
import requests
from gbnf_compiler import *

# Define your Prompt
prompt = "What tool will you use to calculate 2^5 ?"

# Define the LLM Response Template
# Each {{}} is a variable with a rule
template = "I choose {{tool}} because {{reason}}"

tools = MultipleChoice('tool', ['calculator', 'web-search', 'web-browse'])
c = GBNFCompiler(template, { 'tool': tools, 'reason': SingleSentence() })
print(c.grammar())

# Try a dummy result
text = "I choose calculator because it is the most efficient and accurate way to calculate 2^5."
result = c.parse(text)
print(result)

"""
Result: 
{'tool': 'calculator', 'reason': 'it is the most efficient and accurate way to calculate 2^5.'}
"""

# Example: Send it out to local llama.cpp
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
print(c.parse(result))
```

### Useful Rule Examples

1. [`ItemList`](./examples/item_list.py): The Result will automatically compiled into a list of string.
    - Drawback: The LLM might keep generating more items until max tokens.

2. [`Point Form`](./examples/point_form.py): Create a Point Form Result with specific numbers.
    - This can restrict the LLM to provide limited items.