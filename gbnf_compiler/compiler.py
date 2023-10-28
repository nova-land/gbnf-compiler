from typing import List, Dict
from gbnf_compiler.rules import Rule
import re

def flatten_recursive(obj: Rule) -> List[Rule]:
    result = [obj]  # Initialize the result list with the current object
    for item in obj.dependent_rules:
        result.extend(flatten_recursive(item))  # Recursively flatten x
    return result


class GBNFCompiler:
    """Create Grammar String from the template format and also parse the result into dict.
    """
    def __init__(self, template: str, rules: Dict[str, Rule]):
        """Initialise the GBNF Compiler.

        Args:
            template (str): The Template String with handlebars `{{}}` format.
            rules (Dict[str, str]): Each Rule corresponds to each variable.
        """
        # Make sure no variables are stick together which cannot be parsed.
        assert template.replace(' ', '').find('}}{{') == -1

        self.rules = rules
        num_variables = template.count("{{")
        assert len(self.rules) == num_variables
        
        # Create Grammar Format String
        self.template = template
        separated = [split_up.split('}}') for split_up in template.split('{{')]
        separated = [a for b in separated for a in b]
        tokens = separated.copy()
        self.template_tokens = separated.copy()

        for i in range(len(tokens)):
            if ((i+1) %2) == 0:
                tokens[i] = f' {self.rules[tokens[i]].name()} '
            elif len(tokens[i]) > 0:
                # Escape all string quotes
                escaped = tokens[i].replace('"', '\\\"')
                tokens[i] = f'"{escaped}"'
        self.grammar_template = ''.join(tokens)

        # Gather Different Rules
        rule_definitions: dict[str, str] = {}
        for rule in self.rules.values():
            included_rules = flatten_recursive(rule)
            for included_rule in included_rules:
                if included_rule.name() not in rule_definitions:
                    rule_definitions[included_rule.name()] = included_rule.rule
                # Verify all rules has the same definition
                else:
                    assert rule_definitions[included_rule.name()] == included_rule.rule
        
        rule_definitions = '\n'.join(list(rule_definitions.values()))
        self.grammar_str = f'root ::= Template\nTemplate ::= {self.grammar_template}\n{rule_definitions}'

    def grammar(self):
        """Return the GBNF Grammar String for request.

        Returns:
            str: The GBNF Grammar String
        """
        return self.grammar_str

    def parse(self, response: str) -> Dict:
        """Parse the result from LLM response.

        Args:
            response (str): The LLM Response

        Returns:
            dict: The Variable <-> Value Map from the LLM Response.
        """
        escaped_template = re.escape(self.template).replace(r'\{\{', '{{').replace(r'\}\}', '}}')
        pattern = escaped_template.replace('{{', '(?P<').replace('}}', '>(?:.|\n)*?)')

        match = re.fullmatch(pattern, response, re.DOTALL)

        # Return None if the rendered string does not match the template.
        if not match: return None  
        result = match.groupdict()
        # Compile the result for each rule
        for (key, value) in result.items():
            result[key] = self.rules[key].compile(value)
        return result
