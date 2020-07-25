from Tokenize import tokenize
from pprint import pprint
from Analyze import treeBuilder

input_str = input("Enter the expression >>> ")
# Get a list of tokens
token_list = tokenize(input_str)

# Debug - print all tokens with their type and value
# pprint(token_list)

# Get the tree of this expresion
_builder = treeBuilder(token_list)
tree_head = _builder.getHead()

# Debug - print the tree
# _builder.printTree(tree_head)

# Debug - count the tree (no variables)
# value = _builder.countTree(tree_head)
# print("The value is", value)
