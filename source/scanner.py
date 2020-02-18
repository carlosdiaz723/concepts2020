def isAnInteger(input: str):
    '''
    shorthand for testing if a string could be a valid integer
    '''
    try:
        int(input)
        return True
    except ValueError:
        return False


def scan(string: str, keywords=[], doubleSymbols=[]):
    '''
    Input: a string containing the text for a BASIC program
    Output: a list of lexemes scanned from the given text
    '''
    lexeme = ''
    listOfLexemes = []
    # specific flag I used to skip the loop once if a doubleSymbol is found
    doubleFound = False
    # for each character in the string, also keeping track of the index
    for index, character in enumerate(string):
        # true most times, unless the previous loop was a doubleSymbol
        if not doubleFound:
            if character != ' ':
                lexeme += character
            if (index + 1 < len(string)):
                if string[index + 1] == ' ' or string[index + 1] in keywords\
                  or lexeme in keywords:
                    if (lexeme + string[index + 1]) in doubleSymbols:
                        # the special double case
                        lexeme = lexeme + string[index + 1]
                        doubleFound = True
                    if string[index + 1] == '.' and isAnInteger(lexeme) and \
                       isAnInteger(string[index + 2]):
                        # the special '.' inside of float case
                        continue
                    elif lexeme != '':
                        # add to list
                        listOfLexemes.append(lexeme.replace('\n', '<newline>'))
                        lexeme = ''
        else:
            # remove restriction so only one loop is skipped on double case
            doubleFound = False
    return listOfLexemes
