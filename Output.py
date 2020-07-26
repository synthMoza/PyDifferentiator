from Analyze import Node

def latexOutput(original_head : Node, diff_head : Node) -> None:
    """ Outputs the original and diff expression into the latex file """
    
    file = open("output.tex", "w")
    file.write("\\documentclass[12pt, a4paper, oneside]{article}\n")
    file.write("\\usepackage[a4paper, left=20mm, right=10mm, top=20mm, bottom=20mm]{geometry}\n")
    file.write("\\usepackage[utf8]{inputenc}\n")
    file.write("\\usepackage{xcolor}\n")
    file.write("\\usepackage{hyperref}\n")
    file.write("\\usepackage[russian]{babel}\n")
    file.write("    \\title{\\textbf{PyDifferniator v. 0.1}}\n")
    file.write("    \\author{Author: \\href{https://github.com/synthMoza}{synthMoza}}\n")
    file.write("    \\date{\\href{https://github.com/synthMoza/PyDifferentiator}{GitHub Repository}}\n")
    file.write("\\usepackage{graphicx}\n")
    file.write("\\definecolor{linkcolor}{rgb}{0.36, 0.54, 0.66}\n")
    file.write("\\definecolor{urlcolor}{rgb}{0.36, 0.54, 0.66}\n")
    file.write("\\hypersetup{pdfstartview=FitH,  linkcolor=linkcolor,urlcolor=urlcolor, colorlinks=true}\n")
    file.write("\\begin{document}\n")
    file.write("\\maketitle\n")
    file.write("\\thispagestyle{empty}\n")
    file.write("\\par The original expression was:\n")
    file.write("\[f(x) = ")
    latexExp(file, original_head)
    file.write("\]\n")
    file.write("\par The diffiriantiated expression is:\n")
    file.write("\[")
    latexExp(file, diff_head)
    file.write("\]\n")
    file.write("\end{document}")
    file.close()
    
def latexExp(file, _node : Node) -> None:
    """ Recursively prints the expression into the tex file """
    
    if _node.token_t.type == "num" or _node.token_t.type == "var":
        file.write(str(_node.token_t.value))
    elif _node.token_t.type == "op":
        if _node.token_t.value == "+" or _node.token_t.value == "-":
            latexExp(file, _node.children[0])
            file.write(str(_node.token_t.value))
            latexExp(file, _node.children[1])
        elif _node.token_t.value == "*" or _node.token_t.value == "^":
            if _node.children[0].token_t.type == "op" and (_node.children[0].token_t.value == "+" or _node.children[0].token_t.value == "-"):
                file.write("{(")
                latexExp(file, _node.children[0])
                file.write(")}")
            else:
                latexExp(file, _node.children[0])

            if _node.token_t.value == "*":
                file.write("\\cdot ")
            elif _node.token_t.value == "^":
                file.write("^")
            if _node.children[1].token_t.type == "op" and (_node.children[1].token_t.value == "+" or _node.children[1].token_t.value == "-"):
                file.write("{(")
                latexExp(file, _node.children[1])
                file.write(")}")
            else:
                latexExp(file, _node.children[1])
        elif _node.token_t.value == "/":
            file.write("\\frac{")
            latexExp(file, _node.children[0])
            file.write("}")
            file.write("{")
            latexExp(file, _node.children[1])
            file.write("}")
            
        elif _node.token_t.value == "ln" or _node.token_t.value == "sin" or _node.token_t.value == "cos" or _node.token_t.value == "tg" or _node.token_t.value == "ctg":
            file.write(str(_node.token_t.value))
            file.write("{(")
            latexExp(file, _node.children[0])
            file.write(")}")
        else:
            exit("Error! latexExp(): invalid operator " + _node.token_t.value)
    else:
        exit("Error! latexExp(): invalid token type " + _node.token_t.type)




    
