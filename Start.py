from Tokenize import tokenize

input_str = input("Enter the expression >>>")
# Get a list of tokens
token_list = tokenize(input_str)
# Debug
print(token_list)
