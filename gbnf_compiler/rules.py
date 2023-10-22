from typing import List

SINGLE_LINE = 'singleline ::= [^\\n]+ "\\n"'
SINGLE_SENTENCE = 'singlesentence ::= [^.] + "."'

ITEM_RULE = 'item ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'
ITEMLIST_RULE = 'itemlist ::= item+\nitem ::= "- " [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ "\\n"'

STRING_RULE = 'string ::= (^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]))*'
NUMBER_RULE = 'number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)?'

def get_rule_name(rule: str) -> str:
    """Get the Rule's name

    Args:
        rule (str): The GBNF Rule String

    Returns:
        str: The Rule Name
    """
    return rule.split('::=')[0].strip()

def multiple_choice(name: str, choices: List[str]) -> str:
    """Generate the Multiple Choice GBNF Rule

    Args:
        name (str): The Rule Name
        choices (List[str]): The choices

    Returns:
        str: The GBNF Rule string for the multiple choice
    """
    formatted_string = ' | '.join(f'"{item}"' for item in choices)
    formatted_string = f"({formatted_string})"
    return f'{name} ::= {formatted_string}'

