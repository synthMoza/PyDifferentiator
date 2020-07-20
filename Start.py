from Tokenize import tokenize
from Analyze import get_tree

input_str = input("Enter the expression >>>")
# Get a list of tokens
token_list = tokenize(input_str)

# Debug
# print(token_list)

#Get the tree of this expresion
exp_tree = get_tree(token_list)
