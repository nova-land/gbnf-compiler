from __future__ import annotations
from typing import List, Union
import json

class Rule:
    """
    Declaring a Grammar Rule with a custom compiler
    """

    rule: str
    dependent_rules: List[Rule] = []

    def name(self):
        return self.rule.split('::=')[0].strip()
    def compile(self, result: str): return result

class SingleLine(Rule):
    rule = 'singleline ::= [^\\n]+ "\\n"'

class SingleSentence(Rule):
    rule = 'singlesentence ::= [^.] + "."'

class NumberRule(Rule):
    rule = 'number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?'

class StringRule(Rule):
    rule = 'string ::= \"\\"\" ([^"]*) \"\\"\"'

class StringList(StringRule):
    rule = 'stringlist ::= "[]" | "[" string ("," string)* "]"'
    dependent_rules = [StringRule()]

    def compile(self, result: str) -> List[str]:
        return json.loads(result)
    
class NumberList(NumberRule):
    rule = 'numberlist ::= "[]" | "[" number ("," number)* "]"'
    dependent_rules = [NumberRule()]

    def compile(self, result: str) -> List[Union[int, float]]:
        return json.loads(result)

class ItemRule(Rule):
    rule = 'item ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'
    def compile(self, result: str):
        return result.lstrip("- ")
    
class ItemList(Rule):
    rule = 'itemlist ::= item+'
    dependent_rules = [ItemRule()]
    def compile(self, result: str):
        return [x.lstrip("- ") for x in result.split('\n-')]

class MultipleChoice(Rule):
    def __init__(self, name: str, choices: List[str]):
        formatted_string = ' | '.join(f'"{item}"' for item in choices)
        formatted_string = f"({formatted_string})"
        self.rule = f'{name} ::= {formatted_string}'
        super().__init__()

def get_rule_name(rule: str) -> str:
    """Get the Rule's name

    Args:
        rule (str): The GBNF Rule String

    Returns:
        str: The Rule Name
    """
    return rule.split('::=')[0].strip()

