from typing import List

class Rule:
    """
    Declaring a Grammar Rule with a custom compiler
    """

    rule: str
    def name(self):
        return self.rule.split('::=')[0].strip()
    
class BasicRule(Rule):
    dependent_rules: List[Rule] = []
    def compile(self, result: str): return result

class SingleLine(BasicRule):
    rule = 'singleline ::= [^\\n]+ "\\n"'

class SingleSentence(BasicRule):
    rule = 'singlesentence ::= [^.] + "."'

class NumberRule(BasicRule):
    rule = 'number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?'

class StringRule(BasicRule):
    rule = 'string ::= (^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]))*'

class ItemRule(BasicRule):
    rule = 'item ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'
    def compile(self, result: str):
        return result.lstrip("- ")
    
class ItemList(BasicRule):
    rule = 'itemlist ::= item+'
    dependent_rules = [ItemRule()]
    def compile(self, result: str):
        return [x.lstrip("- ") for x in result.split('\n-')]

class MultipleChoice(BasicRule):
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

