from Analyze import Node
from Analyze import isCountable
from Analyze import countTree
from Analyze import printTree

def diffTree(_node : Node) -> Node:
    """ Returns the head node of the tree with the differentiated given expression """
    if _node.token_t.type == "num":
        t_node = Node("0", "num")
        return t_node
    elif _node.token_t.type == "var":
        t_node = Node("1", "num")
        return t_node
    elif _node.token_t.type == "op":
        if _node.token_t.value == "+" or _node.token_t.value == "-":
            t_node = Node(_node.token_t.value, "op")

            for child in _node.children:
                t_node.children.append(diffTree(child))
                
            return t_node
        elif _node.token_t.value == "*":
            mul_node = Node("+", "op")
            l_node = Node("*", "op")
            r_node = Node("*", "op")

            l_node.children.append(_node.children[0].copyNode())
            l_node.children.append(diffTree(_node.children[1].copyNode()))

            r_node.children.append(_node.children[1].copyNode())
            r_node.children.append(diffTree(_node.children[0].copyNode()))
            
            mul_node.children.append(l_node)
            mul_node.children.append(r_node)
            
            return mul_node
        elif _node.token_t.value == "/":
            div_node = Node("/", "op")
            l_node = Node("-", "op")
            l_l_node = Node("*", "op")
            l_r_node = Node("*", "op")
            r_node = Node("*", "op")

            r_node.children.append(_node.children[1].copyNode())
            r_node.children.append(_node.children[1].copyNode())

            l_l_node.children.append(diffTree(_node.children[0].copyNode()))
            l_l_node.children.append(_node.children[1].copyNode())
            l_r_node.children.append(diffTree(_node.children[1].copyNode()))
            l_r_node.children.append(_node.children[0].copyNode())

            l_node.children.append(l_l_node)
            l_node.children.append(l_r_node)
            
            div_node.children.append(l_node)
            div_node.children.append(r_node)
            
            return div_node
    else:
        exit("Error! diffTree(): unknown token type", _node.token_t.type)

def simplifyTree(_node : Node) -> Node:
    """ Simplifies the tree: counts all the inside numbers"""
    if isCountable(_node):
        result = countTree(_node)
        _node = Node(int(result), "num")
        return _node
    else:
        if _node.children:
            for index in range(0, len(_node.children)):
                _node.children[index] = simplifyTree(_node.children[index])
            return _node
        else:
            return _node
                
def simplifyVar(_node : Node) -> Node:
    """ Part of simplification - everything about special cases (like 0 * ... and 1 * ...)) """

    # Debug print
    # print("=====")
    # print("Current token: ", _node.token_t.value)
    # printTree(_node)
    # print("=====")

    if _node.token_t.type == "op":
        if _node.token_t.value == "+":
            if _node.children:
                # 0 + ...
                if _node.children[0].token_t.type == "num" and int(_node.children[0].token_t.value) == 0:
                    return simplifyVar(_node.children[1])
                else:
                    _node.children[0] = simplifyVar(_node.children[0])
                if _node.children[1].token_t.type == "num" and int(_node.children[1].token_t.value) == 0:
                    return simplifyVar(_node.children[0])
                else:
                    _node.children[1] = simplifyVar(_node.children[1])
            else:
                exit("Error! simplifyVar(): Got operation token, but no children")
        elif _node.token_t.value == "-":
            # ... - 0
            if _node.children:
                if _node.children[1].token_t.type == "num" and int(_node.children[1].token_t.value) == 0:
                    return simplifyVar(_node.children[0])
                else:
                    _node.children[0] = simplifyVar(_node.children[0])
                    _node.children[1] = simplifyVar(_node.children[1])
            else:
                exit("Error! simplifyVar(): Got operation token, but no children")
        elif _node.token_t.value == "*":
            if _node.children:
                if _node.children[0].token_t.type == "num" and int(_node.children[0].token_t.value) == 0 or _node.children[1].token_t.type == "num" and int(_node.children[1].token_t.value) == 0:
                    t_node = Node(0, "num")
                    return t_node
                elif _node.children[0].token_t.type == "num" and int(_node.children[0].token_t.value) == 1:
                    return simplifyVar(_node.children[1])
                else:
                    _node.children[0] = simplifyVar(_node.children[0])
                if _node.children[1].token_t.type == "num" and int(_node.children[1].token_t.value) == 1:
                    return simplifyVar(_node.children[0])
                else:
                    _node.children[1] = simplifyVar(_node.children[1])
            else:
                exit("Error! simplifyVar(): Got operation token, but no children")
        elif _node.token_t.value == "/":
            if _node.children:
                if _node.children[0].token_t.type == "num" and int(_node.children[0].token_t.value) == 0:
                    t_node = Node(0, "num")
                    return t_node
                else:
                    _node.children[0] = simplifyVar(_node.children[0])
                if _node.children[1].token_t.type == "num" and int(_node.children[1].token_t.value) == 1:
                    return simplifyVar(_node.children[0])
                else:
                    _node.children[1] = simplifyVar(_node.children[1])
            else:
                exit("Error! simplifyVar(): Got operation token, but no children")
    return _node
