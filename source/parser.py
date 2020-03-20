import tokenizer

tokenList = tokenizer.getAllTokens()

# Prints each item in the tuple object
# Each tuple comes in the following format (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)
for token in tokenList:
    print (token[2], token[4])
    
'''

    Need to create a function for each grammar rule in grammarRules.py 
    each token passed from the tokenList variable to the correct function
    Will be using the top down approach (Recursive Descent) to build the parse tree
    http://effbot.org/zone/simple-top-down-parsing.htm
    
'''

class Parser(object):
    
    def __init__(self, tokens):
        # This will hold all the tokens that have been created by the scanner/lexer
        self.tokens = tokens
        # This will hold the token index we are parsing at
        self.token_index = 0
        
    def parse(self):
        while self.token_index < len(self.tokens):
            
            # Holds the type of tokens for example printable
            token_type = self.tokens[self.token_index][0]
            # Holds the value of tokens for example Y
            token_value = self.tokens[self.token.index][1]
            
            print(token_type, token_value)
            
            #Increment token index by 1 so we can loop through the next totken
            self.token.index += 1