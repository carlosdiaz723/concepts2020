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
THIS IS THE ONLY FILE THAT SHOULD BE RAN.
It should be ran from the 'source' directory.
This is where the list of lexemes is tokenized and printed.

Note: All python files are pep8/pycodestyle compliant.
'''
from scanner import scan
from pprint import pprint as pretty
import re
import lexicalRules


# open example file as a string
with open('example.bas', 'r') as exampleFile:
    ex1 = exampleFile.read()


# gather list of lexemes from scanner.py
lexemes = scan(ex1)


# bool used to short circuit to reduce redundant searching
keywordFound = False
literalFound = False
errorCount = 0


# list of tuplles, tuples in form of:
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
            #print('Lexeme {}: {}'.format(index, lex).ljust(21) +
                  #'Token:Keyword:    {}'.format(key))
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
                #print('Lexeme {}: {}'.format(index, lex).ljust(21) +
                      #'Token:Identifier: {}'.format(key))
                listOfTokens.append((True, index, lex, 'identifier', key))
                errorCount = 0
                literalFound = True
                # break if found, skip to next lexeme
                break
    errorCount += 1
    if errorCount > 1:
        # this will only execute if no possible matches were found
        #print('Lexeme {}: {}'.format(index, lex).ljust(21) +
              #'ERROR: ILLEGAL LEXEME')
        listOfTokens.append((False, index, lex, None, None))
        # reset flag
        literalFound = False
        

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
