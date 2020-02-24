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
This is where the scanner determines what each individual lexeme is. For the
purposes of this assignment, the scanner only FINDS the lexemes, it does NOT
tokenize them. This is the job of the tokenizer. We are aware that it is
possible to tokenize upon finding each lexeme, but have chosen not to so that
the implementation and debugging of the future sections of the interpreter is
easier. Thus, the scanning will be abstracted out from the eyes of the
tokenier, which will produce the desired result.

Note: All python files are pep8/pycodestyle compliant.
'''


'''
list of symbols that are separators, just like whitespace.
'''
symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',', ';',
           '+', '-', '>', '<', '/']


'''
special cases where a keyword is two symbols and might be accidentally
scanned as two different lexemes. As far as we're concerned, BASIC does not
include any of these, but the capability will be left just in case.

We originally included this because SCL DOES have double symbol separators.
'''
doubleSymbols = ['..', ':=']


# SEPARATORS houses all possible special separators
SEPARATORS = symbols + doubleSymbols


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
