from Tokenize import token
from Tokenize import isOperator

# Grammar:
# getHead ::= getPS (PlusSubtraction)
# getPS ::= getMD {[op"+" / op"-"] getMD}*  (MultiplicationDivision)
# getMD ::= getNB {[op"*" / op"/"] getNB}*  (NumberBrackets)
# getNB ::= [num] | {[op"("] getPS [op")"]} 

class Node:
    def __init__(self) -> None:
        self.token_t = token()
        self.children = []
    def setToken(self, _token) -> None:
        """ Sets the value and the type of token of this node """
        self.token_t = _token

class treeBuilder:
    def __init__(self, t_list : list) -> None:
        # List of all tokens
        self.token_list = t_list
        # Current index (current token, if you wish)
        self.list_index = 0
    def currentToken(self) -> Node:
        """ Returns the current token """
        if self.tokenLeft():
            return self.token_list[self.list_index]
        else:
            exit("Error! currentToken(): no tokens left")
    def nextToken(self) -> Node:
        """ Incriment the index of the token list """
        self.list_index += 1
    def tokenLeft(self) -> bool:
        """ Returns true if there are tokens left """
        return self.list_index < len(self.token_list)
    def isOperator(self, op : chr) -> bool:
        """ Returns true if the current token is the given and supported operator, false if not"""
        if self.tokenLeft():
            return self.currentToken().value == op and self.currentToken().type == "op"
        else:
            return False
    def isNumber(self) -> bool:
        """ Returns true if the current token is a number, false if not """
        if self.tokenLeft():
            return self.currentToken().type == "num"
        else:
            return False
    def errExp(self, exp) -> None:
        """ Throws an error on what was expected and what we got, then exits """
        print("Error!")
        if self.tokenLeft():
            exit("Expected \"" + str(exp) + "\", got \"" + str(self.currentToken().value) + "\".")
        else:
            exit("Expected \"" + str(exp) + "\", got nothing.")
    def printTree(self, _node) -> None:
        """ Prints the tree recursively - for debug purposes only"""
        if _node.children:
            # If there are children in this node
            self.printTree(_node.children[0])
            print(_node.token_t.value)
            self.printTree(_node.children[1])   
        else:
            print(_node.token_t.value)
    def countTree(self, _node) -> int:
        """ Counts the given tree (no variable!!!) """
        result = 0
        
        if _node.token_t.type == "op":
            # We got the operation
            if _node.token_t.value == "+":
                # Sum
                for child in _node.children:
                    result += self.countTree(child)
            elif _node.token_t.value == "-":
                # Subtraction
                
                result = self.countTree(_node.children[0]) - self.countTree(_node.children[1])
            elif _node.token_t.value == "*":
                # Multiplication
                result = 1
                
                for child in _node.children:
                    result *= self.countTree(child)
            elif _node.token_t.value == "/":
                # Division
                
                result = self.countTree(_node.children[0]) / self.countTree(_node.children[1])
            else:
                exit("Error! Unknown operation:", _node.token_t.value)

            # Debug print - temp result and current token
            # print("Current token is", _node.token_t)
            # print("Current result is", result)
            return result
        elif _node.token_t.type == "num":
            result = _node.token_t.value
            
            # Debug print - temp result and current token
            # print("Current token is", _node.token_t)
            # print("Current result is", result)
            return result
        else:
            exit("Error! Unknown token type:", _node.token_t.type)
    # The following functions are the rules of this grammar. Check the first lines of this module.
    def getHead(self) -> Node:
        # getHead ::= getPS (PlusSubtraction)

        # Debug print
        # print("Current rule is getHead(), current token", self.currentToken())
        return self.getPS()
    def getPS(self) -> Node:
        # getPS ::= getMD {[op"+" / op"-"] getMD}*  (MultiplicationDivision)

        # Debug print
        # print("Current rule is getPS(), current token", self.currentToken())
        _node = self.getMD()
        _node_left = Node()
        _node_right = Node()
                  
        while self.isOperator("+") or self.isOperator("-"):
            _node_left = _node
            _node = Node()

            # Debug print
            # print("Current rule is getPS(), current token", self.currentToken())
            _node.setToken(self.currentToken())
            self.nextToken()
            _node_right = self.getMD()
            
            _node.children.append(_node_left)
            _node.children.append(_node_right)
            
        return _node
            
    def getMD(self) -> Node:
        # getMD ::= getNB {[op"*" / op"/"] getNB}*  (NumberBrackets)

        # Debug print
        # print("Current rule is getMD(), current token", self.currentToken())
        _node = self.getNB()
        _node_left = Node()
        _node_right = Node()
                  
        while self.isOperator("*") or self.isOperator("/"):
            _node_left = _node
            _node = Node()

            _node.setToken(self.currentToken())
            self.nextToken()

            # Debug print
            # print("Current rule is getMD(), current token", self.currentToken())
            _node_right = self.getNB()
            
            _node.children.append(_node_left)
            _node.children.append(_node_right)
            
        return _node
    def getNB(self) -> Node:
        # getNB ::= [num] | {[op"("] getPS [op")"]}

        # Debug print
        # print("Current rule is getNB(), current token", self.currentToken())
        if self.isNumber():
            _node = Node()
            _node.setToken(self.currentToken())
            self.nextToken()
            return _node
        else:
            if self.isOperator("("):
                self.nextToken()
                _node = self.getPS()
                if self.isOperator(")"):
                    self.nextToken()
                    return _node
                else:
                    self.errExp(") or number")
            else:
                self.errExp("( or number")

        
