from typing import List, Dict
from itertools import product
from gbnf_compiler.rules import get_rule_name

def get_all_occurrence_ends(sub: str, a_str: str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start + len(sub)
        start += 1

def is_ascending_sequence(seq: List[int]):
    if seq == []: return True
    for i in range(1, len(seq)):
        if seq[i] <= seq[i-1]: return False
    return True

def get_values_lengths(dictionary: Dict):
    # Calculate the sum of the lengths of values in the dictionary
    return sum(map(lambda value: len(value), dictionary.values()))
    # return sum(len(value) for value in dictionary.values())
    # return Object.values(dictionary).reduce((sum, value) => sum + value.length, 0);

def sort_by_longest_values(dictionaries: List[Dict]):
    # Sort dictionaries by the sum of the lengths of their values and return the longest one
    sorted_dicts = sorted(dictionaries, key=lambda d: get_values_lengths(d), reverse=True)
    return sorted_dicts[0] if sorted_dicts else None

class GBNFCompiler:
    """Create Grammar String from the template format and also parse the result into dict.
    """
    def __init__(self, template: str, rules: Dict[str, str]):
        """Initialise the GBNF Compiler.

        Args:
            template (str): The Template String with handlebars `{{}}` format.
            rules (Dict[str, str]): Each Rule corresponds to each variable.
        """
        assert template.find('}}{{') == -1

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
                tokens[i] = f' {get_rule_name(self.rules[tokens[i]])} '
            elif len(tokens[i]) > 0:
                # Escape all string quotes
                escaped = tokens[i].replace('"', '\\\"')
                tokens[i] = f'"{escaped}"'
        self.grammar_template = ''.join(tokens)

        # Gather Different Rules
        rule_definitions = {}
        for rule in self.rules.values():
            rule_name = get_rule_name(rule)
            if rule_name not in rule_definitions:
                rule_definitions[rule_name] = rule
            # Verify all rules has the same definition
            else:
                assert rule_definitions[rule_name] == rule
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
        # Get Text & Placeholders
        template_text = [v for index, v in enumerate(self.template_tokens) if index % 2 == 0 and v]
        template_placeholders = [v for index, v in enumerate(self.template_tokens) if index % 2 != 0 and v]

        # Get all ocurrences of all template text parts
        part_occurrences = [list(get_all_occurrence_ends(part, response)) for part in template_text]
        
        # Get all combinations with an element
        comb_occurrences = product(*part_occurrences)
        comb_occurrences = filter(is_ascending_sequence, comb_occurrences)
        # trick for later use
        template_text.append('')

        # Get all potential candidates for the placeholders
        potential_placeholders = []
        for placeholder_indices in comb_occurrences:
            potential_slot = []
            template_index = 0
            if placeholder_indices[0] > 0:
                # Text before the 1st placeholder in template, skip
                template_index = 1

            for i in range(len(placeholder_indices)):
                placeholder_index = placeholder_indices[i]
                if (i+1) >= len(placeholder_indices):
                    next_placeholder_index = len(response)
                else:
                    next_placeholder_index = placeholder_indices[i+1]

                slicedText = response[placeholder_index:(next_placeholder_index - len(template_text[template_index]))]
                potential_slot.append(slicedText)
                template_index += 1
            potential_placeholders.append(potential_slot)


        to_return = []
        for placeholders in potential_placeholders:
            # match the placeholder names onto the potential placeholders
            matched_placeholders = {key: placeholders[index] for index, key in enumerate(template_placeholders)}
            to_return.append(matched_placeholders)

        # Get the one with longest values
        return sort_by_longest_values(to_return)
