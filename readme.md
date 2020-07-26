The documentation conforms to the latest version  
# What is this?  
This is a simple app that allows you to diffirintiate the expression
# Syntax  
Allowed operations are: +, -, /, *
For variables you should use only "x"
# How it works?  
The algorithm is simple: at first, the expression is being tokenized, then the tree is build based on the token list, and after this the tree is being diffirintiated recursively. After simple simplification, it is shown in the console
# Additional functions  
For debugging purposes (or not), I created some extra useful functions:
- 'countTree() - counts the value of the given expression tree (if there are variables, exits with an error)
- beautiful output of the class "token" with its value and type
- 'printTree() - returns the string with the expression of this tree recursively. It si a temporary output function  

# Special Thanks  
I want to say thanks to the person who wrote this code - myself  
