'''
Names / Emails:
Carlos Diaz             cdiaz29@students.kennesaw.edu
Benjamin Cervantes     bcervan4@students.kennesaw.edu
Aydan Mufti             amufti1@students.kennesaw.edu


College of Computing and Software Engineering
Department of Computer Science
---------------------------------------------
CS4308: CONCEPTS OF PROGRAMMING LANGUAGES
SECTION W01 – SPRING 2020
---------------------------------------------
Course Project
1st Deliverable: Scanner


File Description:
This is where the source .bas file is scanned and tokenized.

Note: All python files are pep8/pycodestyle compliant.
'''
import re
import lexicalRules


# list of symbols that are separators, just like whitespace.
symbols = ['{', '}', '(', ')', '[', ']', '.', '*', '\n', ':', ',', ';',
           '+', '-', '>', '<', '/']
doubleSymbols = ['..', ':=']


# SEPARATORS houses all possible special separators
SEPARATORS = symbols + doubleSymbols


def getAllTokens():
    '''
    Will return the entire list of tuples containing information about each
    lexeme/token.

    Each tuple is of form:
    (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)

    Example:
    (True, 2, 'if', 'keyword', 'IF')

    Invalid tokens are of form:
    (False, lexemeNumber, lexeme, None, None)
    '''
    return listOfTokens


def getToken(n: int):
    '''
    Returns the nth tuple in the list.

    Each tuple is of form:
    (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)

    Example:
    (True, 2, 'if', 'keyword', 'IF')

    Invalid tokens are of form:
    (False, lexemeNumber, lexeme, None, None)
    '''
    return listOfTokens[n]


def isAnInteger(input: str):
    '''
    Creating shorthand for testing if a string could be a valid integer
    '''
    try:
        int(input)
        return True
    except ValueError:
        return False


def scan(string: str):
    '''
    Input: a string containing the text for a BASIC program
    Output: a list of lexemes scanned from the given text
    '''
    lexeme = ''
    listOfLexemes = []
    # specific flag used to skip the loop once if a doubleSymbol is found
    doubleFound = False
    # for each character in the string, also keeping track of the index
    for index, character in enumerate(string):
        # true most times, unless the previous loop was a doubleSymbol
        if not doubleFound:
            if character != ' ':
                lexeme += character
            if index + 1 == len(string):
                listOfLexemes.append(lexeme)
                return listOfLexemes
            if (index + 1 < len(string)):
                if string[index + 1] == ' ' or string[index + 1] in SEPARATORS\
                        or lexeme in SEPARATORS:
                    if (lexeme + string[index + 1]) in doubleSymbols:
                        # the special doubleSymbol case
                        lexeme = lexeme + string[index + 1]
                        listOfLexemes.append(lexeme)
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


# open example file as a string
with open('example.bas', 'r') as exampleFile:
    ex1 = exampleFile.read()


# gather list of lexemes from scanner.py
lexemes = scan(ex1)


# bool used to short circuit to reduce redundant searching
keywordFound = False
literalFound = False
errorCount = 0


# list of tuples, tuples in form of:
# (validity(true/false), lexemeNumber, lexeme, tokenType(id/keyword), token)
listOfTokens = list(tuple())


# loop through each lexeme and keep track of index
for index, lex in enumerate(lexemes):
    keywordFound = False
    # check all keywords first
    for key in lexicalRules.keywords:
        # attempt to match lex with a keyword
        x = re.search(lexicalRules.keywords[key], lex)
        if x is not None:
            listOfTokens.append((True, index, lex, 'keyword', key))
            keywordFound = True
            errorCount = 0
            # break if found, skip to next lexeme
            break
    # if no keyword matches, check if a literal
    if not keywordFound:
        for key in lexicalRules.literals:
            y = re.search(lexicalRules.literals[key], lex)
            if y is not None:
                listOfTokens.append((True, index, lex, 'identifier', key))
                errorCount = 0
                literalFound = True
                # break if found, skip to next lexeme
                break
    errorCount += 1
    if errorCount > 1:
        listOfTokens.append((False, index, lex, None, None))
        # reset flag
        literalFound = False
