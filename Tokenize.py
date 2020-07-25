from sys import exit

# The list of all supported operators and delimiters
operators = ['+', '-', '*', '/', '(', ')']
delimiters = [' ', '\n','\t']

# Token class that has its type (operation or number) and value
# Avalible token types: "num", "op", "var"
# "var" - only supported "x"
class token:
    def __init__(self) -> None:
        self.value = 0
        self.type = ""
    def __repr__(self) -> str:
        """ For debugging purposes only - represents as its value"""
        return "Type: " + str(self.type) + "\tValue: " + str(self.value)

def isOperator(sym : chr) -> bool:
    """ Return true if the given symbol is a supported operator, false if not """
    if sym in operators:
        return True
    else:
        return False

def isVariable(sym : chr) -> bool:
    """ Return true if the given symbol is a supported variable, false if not """
    return sym == "x"

def isDelimiter(sym : chr) -> bool:
    """ Return true if the given symbol is a delimiter, false if not """
    if sym in delimiters:
        return True
    else:
        return False
    
def tokenize(input_str : str) -> list:
    """ Tokenizes the given string - returns the list of tokens (see class token)"""
    # The result list and the temp variable for numbers
    result = []
    raw_number = ""

    # Add an extra space for tokenizing the last number properly
    input_str += delimiters[0]

    for sym in input_str:
        if not sym.isdigit() and len(raw_number) != 0:
            # Create a number token
            _token = token()
            _token.value = int(raw_number)
            _token.type = "num"
            result.append(_token)
            raw_number = ""
        if isOperator(sym):
            # Create an operator token
            _token = token()
            _token.value = sym
            _token.type = "op"
            result.append(_token)
        elif isDelimiter(sym):
            # Skip unneccessary symbols
            continue
        elif isVariable(sym):
            _token = token()
            _token.type = "var"
            _token.value = sym
            result.append(_token)
        elif sym.isdigit():
            # Prepare the number for futher tokenization
            raw_number += sym
        else:
            exit("Fatal error: unknown symbol: " + sym)

    return result
