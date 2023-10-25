from typing import List

class Rule:
    """
    Declaring a Grammar Rule with a custom compiler
    """

    rule: str
    def compile(self, result: str): return result
    def name(self):
        return self.rule.split('::=')[0].strip()

class SingleLine(Rule):
    rule = 'singleline ::= [^\\n]+ "\\n"'

class SingleSentence(Rule):
    rule = 'singlesentence ::= [^.] + "."'

class NumberRule(Rule):
    rule = 'number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?'

class StringRule(Rule):
    rule = 'string ::= (^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]))*'

class ItemRule(Rule):
    rule = 'item ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'
    def compile(self, result: str):
        return result.lstrip("- ")
    
class ItemList(Rule):
    rule = 'itemlist ::= item+\nitem ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'
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

