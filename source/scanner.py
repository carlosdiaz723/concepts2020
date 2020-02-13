from pprint import pprint as pretty
# using this to print lists in a prettier format

'''
basic Scanner logic:
    -' ' is seperator (space or tab)                [DONE]
    -certain symbols are also seperators            [DONE]
    -scan each instance between ' ' or a seperator  [DONE]
congrats, you have all the lexemes
now, tokenize
    -scan each lexeme
    -determine token

'''


def isAnInteger(input: str):
    '''
    shorthand for testing if a string could be a valid integer
    '''
    try:
        int(input)
        return True
    except ValueError:
        return False


ex1 = ""
with open('./../example.txt', 'r') as exampleFile:
    ex1 = exampleFile.read()
'''
list of symbols that are seperators, just like whitespace.
they'll all be lexemes except sometimes '.' will be inside of a float.
'''
symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',', ';',
           '+', '-', ]


'''
special cases where a keyword is two symbols and might be accidentally
scanned as two different lexemes. I've tried to code out this possibility but
we might run into problems later.
'''
doubleSymbols = ['..', ':=']

# KEYWORDS houses all possible special seperators (hopefully, i dont know SCL)
KEYWORDS = symbols + doubleSymbols


def scan(string: str):
    '''
    Input: a string containing the text for an SCL program
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
                if string[index + 1] == ' ' or string[index + 1] in KEYWORDS\
                  or lexeme in KEYWORDS:
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


# print it out, optional but cool to see for now
for index, lex in enumerate(scan(ex1)):
    print('Lexeme ', (index + 1), ':  ', lex, sep='')
