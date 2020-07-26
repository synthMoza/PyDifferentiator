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
        # (x)' = 1
        
        t_node = Node("1", "num")
        return t_node
    elif _node.token_t.type == "op":
        # Diff operators
        if _node.token_t.value == "+" or _node.token_t.value == "-":
            # (f +- g)' = f' +- g'
            t_node = Node(_node.token_t.value, "op")

            if _node.children:
                for child in _node.children:
                    t_node.children.append(diffTree(child))
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
                
            return t_node
        elif _node.token_t.value == "*":
            # (f*g)' = f'*g + f * g'
                
            mul_node = Node("+", "op")
            l_node = Node("*", "op")
            r_node = Node("*", "op")

            if _node.children:
                l_node.children.append(_node.children[0].copyNode())
                l_node.children.append(diffTree(_node.children[1].copyNode()))

                r_node.children.append(_node.children[1].copyNode())
                r_node.children.append(diffTree(_node.children[0].copyNode()))
                
                mul_node.children.append(l_node)
                mul_node.children.append(r_node)
                
                return mul_node
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        elif _node.token_t.value == "/":
            # (f / g )' = (f'*g - f * g')/ g^2
            
            div_node = Node("/", "op")
            l_node = Node("-", "op")
            l_l_node = Node("*", "op")
            l_r_node = Node("*", "op")
            r_node = Node("*", "op")

            if _node.children:
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
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        elif _node.token_t.value == "^":
            # (f^g)' = f^g(g'*ln(f)+g/f)

            pow_node = Node("*", "op")
            l_pow_node = Node("^", "op")
            r_pow_node = Node("+", "op")
            r_l_pow_node = Node("*", "op")
            ln_node = Node("ln", "op")
            r_r_pow_node = Node("/", "op")

            if _node.children:
                r_r_pow_node.children.append(_node.children[1].copyNode())
                r_r_pow_node.children.append(_node.children[0].copyNode())
                r_l_pow_node.children.append(diffTree(_node.children[1].copyNode()))
                ln_node.children.append(_node.children[0]. copyNode())
                r_l_pow_node.children.append(ln_node)
                r_pow_node.children.append(r_l_pow_node)
                r_pow_node.children.append(r_r_pow_node)
                l_pow_node.children.append(_node.children[0].copyNode())
                l_pow_node.children.append(_node.children[1].copyNode())

                pow_node.children.append(l_pow_node)
                pow_node.children.append(r_pow_node)
                
                return pow_node
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        elif _node.token_t.value == "ln":
            # (ln f)' =f' / f
            
            ln_node = Node("/", "op")

            if _node.children:
                ln_node.children.append(diffTree(_node.children[0].copyNode()))
                ln_node.children.append(_node.children[0].copyNode())

                return ln_node
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        elif _node.token_t.value == "sin":
            # (sin f)' = cos f * f'
            
            sin_node = Node("*", "op")
            sin_l_node = Node("cos", "op")

            if _node.children:
                sin_l_node.children.append(_node.children[0].copyNode())
                sin_node.children.append(sin_l_node)
                sin_node.children.append(diffTree(_node.children[0].copyNode()))

                return sin_node
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        elif _node.token_t.value == "cos":
            # (cos f)' = -1*sin f * f'
            
            cos_node = Node("*", "op")
            cos_r_node = Node("*", "op")
            cos_l_node = Node("sin", "op")

            if _node.children:
                cos_r_node.children.append(Node("-1", "num"))
                cos_l_node.children.append(_node.children[0].copyNode())
                cos_r_node.children.append(cos_l_node)
                cos_node.children.append(cos_r_node)
                cos_node.children.append(diffTree(_node.children[0].copyNode()))

                return cos_node
            else:
                exit("Error! diffTree(): no children for operator " + _node.token_t.value)
        else:
            exit("Error! diffTree(): unknown operator " + _node.token_t.value)
    else:
        exit("Error! diffTree(): unknown token type " + _node.token_t.type)

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
