import tokenizer

tokenList = tokenizer.getAllTokens()

# Prints each item in the tuple object
# Each tuple comes in the following format (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)
for token in tokenList:
    print (tokenList.index(token), token)
    
'''

    Need to create a function for each grammar rule in grammarRules.py 
    each token passed from the tokenList variable to the correct function
    Will be using the top down approach (Recursive Descent) to build the parse tree
    http://effbot.org/zone/simple-top-down-parsing.htm
    
'''
