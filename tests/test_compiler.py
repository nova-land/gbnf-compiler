from gbnf_compiler.compiler import GBNFCompiler
from gbnf_compiler.rules import *

def test_simple_grammar():

    template = "Here is a {{thing}} for you: {{smiley}}"
    text = "Here is a smiley for you: :-)"
    c = GBNFCompiler(template, { 'thing': SingleLine(), 'smiley': SingleLine() })
    result = c.parse(text)

    assert result['thing'] == 'smiley'
    assert result['smiley'] == ':-)'

def test_simple_json():
    import json
    template = json.dumps({ 'objective': "{{objective}}", 'first_goal': "{{first_goal}}", 'second_goal': "{{second_goal}}" })
    c = GBNFCompiler(template, { 'objective': SingleSentence(), 'first_goal': SingleSentence(), 'second_goal': SingleSentence() })

    expect_grammar = r'''root ::= Template
Template ::= "{\"objective\": \"" singlesentence "\", \"first_goal\": \"" singlesentence "\", \"second_goal\": \"" singlesentence "\"}"
singlesentence ::= [^.] + "."'''

    assert expect_grammar == c.grammar()

    text = '{"objective": ">To provide valuable insights and data-driven recommendations to help the cute pet snack startup grow and succeed in the market.", "first_goal": ">To gather and analyze information about the target market, including consumer behavior, preferences, and needs.", "second_goal": ">To assess the competitive landscape and identify opportunities for differentiation and innovation."}'
    result = c.parse(text)

    assert result['objective'] == ">To provide valuable insights and data-driven recommendations to help the cute pet snack startup grow and succeed in the market."
    assert result['first_goal'] == ">To gather and analyze information about the target market, including consumer behavior, preferences, and needs."
    assert result['second_goal'] == ">To assess the competitive landscape and identify opportunities for differentiation and innovation."


# Testing multiple choice rule
def test_multiple_choice():
    template = "I choose {{tool}} because {{reason}}"
    text = "I choose calculator because I need to calculate the result of 2^5."
    tools = MultipleChoice('tool', ['calculator', 'web-search', 'web-browse'])

    c = GBNFCompiler(template, { 'tool': tools, 'reason': SingleSentence() })

    expect_grammar = r'''root ::= Template
Template ::= "I choose " tool " because " singlesentence 
tool ::= ("calculator" | "web-search" | "web-browse")
singlesentence ::= [^.] + "."'''

    assert c.grammar() == expect_grammar

    result = c.parse(text)
    expect_result = {'tool': 'calculator', 'reason': 'I need to calculate the result of 2^5.'}
    assert result == expect_result

def test_item_list():
    template = "Objectives: {{objectives}}"
    text = r'''Objectives: - Objective 1
- Objective 2
- Objective 3
- Objective 4'''

    c = GBNFCompiler(template, { 'objectives': ItemList() })
    expect_grammar = r'''root ::= Template
Template ::= "Objectives: " itemlist 
itemlist ::= item+
item ::= "- " [^\r\n\x0b\x0c\x85\u2028\u2029]+ "\n"'''

    assert c.grammar() == expect_grammar

    result = c.parse(text)
    expect_result = {'objectives': ['Objective 1', 'Objective 2', 'Objective 3', 'Objective 4']}
    assert result == expect_result