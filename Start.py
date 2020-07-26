from pprint import pprint
from Tokenize import tokenize
from Analyze import treeBuilder
from Analyze import countTree
from Analyze import printTree
from Diff import diffTree
from Diff import simplifyTree
from Diff import simplifyVar

print("============================================")
print("\tPyDifferiantiator v. 0.0")
print("============================================")
input_str = input("Enter the expression >>> ")
# Get a list of tokens
token_list = tokenize(input_str)

# Debug - print all tokens with their type and value
# pprint(token_list)

# Get the tree of this expresion
_builder = treeBuilder(token_list)
tree_head = _builder.getHead()

# Debug - print the original tree
# print("The original tree")
# print(printTree(tree_head))

diff_head = diffTree(tree_head)

for i in range(1, 4):
    diff_head = simplifyVar(diff_head)
    # print("Debug")  
    # print(printTree(diff_head))
    diff_head = simplifyTree(diff_head)

# Temp output - prints the simplified tree
print("The result expression is")
print(printTree(diff_head))


# Debug - count the tree (no variables)
# value = countTree(tree_head)
# print("The value is", value)
