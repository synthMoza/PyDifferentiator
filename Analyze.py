from Tokenize import token
from Tokenize import isOperator
from math import log1p
from math import sin
from math import cos

# Grammar:
# getHead ::= getPS (PlusSubtraction)
# getPS ::= getMD {[op"+" / op"-"] getMD}*  (MultiplicationDivision)
# getMD ::= getPW {[op"*" / op"/"] getPW}*  (NumberBrackets)
# getPW ::= getNB {[op"^"] getNB}* (Power)
# getNB ::= [num] | {[op"ln" / op"sin" / op"cos" / op"tg" / op"ctg"]}? {[op"("] getPS [op")"]} 

class Node:
    def __init__(self, _value = 0, _type = "") -> None:
        self.token_t = token(_value, _type)
        self.children = []
    def setToken(self, _token) -> None:
        """ Sets the value and the type of token of this node """
        self.token_t = _token
    def copyNode(self):
        """ Returns the copy of this node """
        _node = Node(self.token_t.value, self.token_t.type)
        _node.children = self.children.copy()

        return _node
    def isEmpty(self) -> bool:
        """ Returns true if this node has no token in it, otherwise returns false """
        return self.token_t.type == ""
def printTree(_node) -> str:
        """ Returns the string of the tree recursively - for debug purposes only"""
        result = ""
        
        if len(_node.children) == 1:
            result += str(_node.token_t.value)
            result += "("
            result += printTree(_node.children[0])
            result += ")"
        elif len(_node.children) == 2:
            result += "("
            result += printTree(_node.children[0])
            result += str(_node.token_t.value)
            result += printTree(_node.children[1])
            result += ")"
        elif len(_node.children) == 0:
            result = str(_node.token_t.value)
        else:
            exit("Error! printTree(): too many children")
        return result
            
def isCountable(_node) -> bool:
        """ Returns true if the tree is countable (there are no variables) """
        result = True
        
        if _node.token_t.type == "var":
            result = False
        else:
            if _node.children:
                for child in _node.children:
                    result = (result and isCountable(child))
            else:
                result = True

        # Debug print
        # printTree(_node)
        # print(result)
        # print("========================")

        return result

def countTree(_node) -> int:
        """ Counts the given tree (no variable!!!) """
        result = 0

        if _node.token_t.type == "op":
            # We got the operation
            if _node.token_t.value == "+":
                # Sum
                for child in _node.children:
                    result += countTree(child)
            elif _node.token_t.value == "-":
                # Subtraction
                
                result = countTree(_node.children[0]) - countTree(_node.children[1])
            elif _node.token_t.value == "*":
                # Multiplication
                result = 1
                
                for child in _node.children:
                    result *= countTree(child)
            elif _node.token_t.value == "/":
                # Division

                sub = countTree(_node.children[1])

                if sub != 0:
                    result = countTree(_node.children[0]) / sub
                else:
                    exit("Error! countTree(): divishion by zero")
            elif _node.token_t.value == "^":
                # Power

                result = countTree(_node.children[0]) ** countTree(_node.children[1])
            elif _node.token_t.value == "ln":
                # Ln

                result = log1p(countTree(_node.children[0]) - 1)
            elif _node.token_t.value == "sin":
                # Sin

                result = sin(countTree(_node.children[0]))
            elif _node.token_t.value == "cos":
                # Sin

                result = cos(countTree(_node.children[0]))
            else:
                exit("Error! Unknown/uncountable operation: " + _node.token_t.value)

            # Debug print - temp result and current token
            # print("Current token is", _node.token_t)
            # print("Current result is", result)
            return result
        elif _node.token_t.type == "num":
            result = int(_node.token_t.value)
            
            # Debug print - temp result and current token
            # print("Current token is", _node.token_t)
            # print("Current result is", result)
            return result
        else:
            exit("Error! Unknown token type " + _node.token_t.type)
             

class treeBuilder:
    def __init__(self, t_list : list = []) -> None:
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
    def isVar(self) -> bool:
        """ Returns true if the current token is a variable, false if not """
        if self.tokenLeft():
            return self.currentToken().type == "var"
        else:
            return False
    def errExp(self, exp) -> None:
        """ Throws an error on what was expected and what we got, then exits """
        print("Error!")
        if self.tokenLeft():
            exit("Expected \"" + str(exp) + "\", got \"" + str(self.currentToken().value) + "\".")
        else:
            exit("Expected \"" + str(exp) + "\", got nothing.")
       
    # The following functions are the rules of this grammar. Check the first lines of this module.
    def getHead(self) -> Node:
        # getHead ::= getPS (PlusSubtraction)

        # Debug print
        # print("Current rule is getHead(), current token", self.currentToken())

        if self.token_list:
            return self.getPS()
        else:
            exit("Error! getHead(): empty expression")
    def getPS(self) -> Node:
        # getPS ::= getMD {[op"+" / op"-"] getMD}*

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
        # getMD ::= getPW {[op"*" / op"/"] getPW}*

        # Debug print
        # print("Current rule is getMD(), current token", self.currentToken())
        _node = self.getPW()
        _node_left = Node()
        _node_right = Node()
                  
        while self.isOperator("*") or self.isOperator("/"):
            _node_left = _node
            _node = Node()

            _node.setToken(self.currentToken())
            self.nextToken()

            # Debug print
            # print("Current rule is getMD(), current token", self.currentToken())
            _node_right = self.getPW()
            
            _node.children.append(_node_left)
            _node.children.append(_node_right)
            
        return _node
    
    def getPW(self) -> Node:
        # getPW ::= getNB {[op"^"] getNB}* (Power)

        # Debug print
        # print("Current rule is getPW(), current token", self.currentToken())
        _node = self.getNB()
        _node_left = Node()
        _node_right = Node()
                  
        while self.isOperator("^"):
            _node_left = _node
            _node = Node()

            # Debug print
            # print("Current rule is getPW(), current token", self.currentToken())
            _node.setToken(self.currentToken())
            self.nextToken()
            _node_right = self.getNB()
            
            _node.children.append(_node_left)
            _node.children.append(_node_right)
        return _node
            
    def getNB(self) -> Node:
        # getNB ::= [num] | {[op"ln" / op"sin" / op"cos" / op"tg" / op"ctg"]}? {[op"("] getPS [op")"]} 

        # Debug print
        # print("Current rule is getNB(), current token", self.currentToken())
        if self.isNumber() or self.isVar():
            _node = Node()
            _node.setToken(self.currentToken())
            self.nextToken()
            return _node
        else:
            _node = Node()
            t_node = Node()
            
            if self.isOperator("ln") or self.isOperator("sin") or self.isOperator("cos") or self.isOperator("tg") or self.isOperator("ctg"):
                t_node.setToken(self.currentToken()) 
                self.nextToken()    
            if self.isOperator("("):
                self.nextToken()
                _node = self.getPS()
                if self.isOperator(")"):
                    self.nextToken()
                else:
                    self.errExp(") or number")
            else:
                self.errExp("( or number")
            if t_node.isEmpty():
                return _node
            else:
                t_node.children.append(_node)
                return t_node

        
