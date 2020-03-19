import tokenizer

tokenList = tokenizer.getAllTokens()

# Prints each item in the tuple object
# Each tuple comes in the following format (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)
for token in tokenList:
    print (tokenList.index(token), token)
    
'''

    Need to create function to parse each token passed in by tokenList and begin creating parse tree
    Will be using the top down approach (Recursive Descent) to build the parse tree
    
'''
