import Tokenize

# Temporary grammar:
# getHead ::= getPS (PlusSubtraction)
# getPS ::= getMD {[op"+" / op"-"] getMD}*  (MultiplicationDivision)
# getMD ::= getNB {[op"*" / op"/"] getNB}*  (NumberBrackets)
# getNB ::= [num] | {[op"("] getPS [op")"]} 
#
#
#
#

class Node:
    def __init__(self) -> None:
        self.token = token()
        self.leftChild = 0
        self.rightChild = 0

def get_tree(token_list : list) -> Node:
    
