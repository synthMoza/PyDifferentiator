The documentation conforms to the latest version  (version 0.1)  
# What is this?  
This is a simple app that allows you to diffirintiate the expression and see it in latex file  
# Syntax  
Allowed operations are: +, -, /, \*, ^, ln, sin, cos, tg, ctg    
For variables you should use only "x"  
# How to use?  
If you use Linux, you can use the Makefile by typing in terminal (in the project directory):  
> make

Makefil compiles the program, asks you to enter the expression in the console, then outputs the result into the output.tex, compiles it and opens the ``.pdf`` file, deleting temporary tex files.  

If you use Windows or Makefile doesn't work, you can compile by yourself and compile LaTeX file (example for Linux):  
> python3 Start.py
> pdflatex output.tex output.pdf

To open it, you may use any pdf program(for example on Linux you may use):  
> xdg-open output.pdf

# How it works?  
The algorithm is simple: at first, the expression is being tokenized, then the tree is build based on the token list, and after this the tree is being diffirintiated recursively. After simple simplification, this tree is put into a simple latex file and opens it.

# Additional functions  
For debugging purposes (or not), I created some extra useful functions:  
- ``countTree()`` - counts the value of the given expression tree (if there are variables, exits with an error)  
- beautiful output of the class "token" with its value and type  
- ``printTree()`` - returns the string with the expression of this tree recursively. It si a temporary output function  

# Special Thanks  
I want to say thanks to the person who wrote this code - myself.  
