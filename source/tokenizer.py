from scanner import scan
import re
import lexicalRules


with open('./../example.txt', 'r') as exampleFile:
    ex1 = exampleFile.read()


'''
list of symbols that are seperators, just like whitespace.
they'll all be lexemes except sometimes '.' will be inside of a float.
'''
symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',', ';',
           '+', '-', '>', '<', '/']


'''
special cases where a keyword is two symbols and might be accidentally
scanned as two different lexemes. I've tried to code out this possibility but
we might run into problems later.
'''
doubleSymbols = ['..', ':=']


# SEPARATORS houses all possible special seperators
SEPARATORS = symbols + doubleSymbols


# print it out, optional but cool to see for now
lexemes = scan(ex1, SEPARATORS, doubleSymbols)

keywordFound = False

for index, lex in enumerate(lexemes):
    keywordFound = False
    for key in lexicalRules.keywords:
        x = re.search(lexicalRules.keywords[key], lex)
        if x is not None:
            print('Lexeme {}: {}'.format(index + 1, lex).ljust(25) +
                  'Token: {}'.format(key))
            keywordFound = True
            break
    if not keywordFound:
        for key in lexicalRules.literals:
            y = re.search(lexicalRules.literals[key], lex)
            if y is not None:
                print('Lexeme {}: {}'.format(index + 1, lex).ljust(25) +
                      'Token: {}'.format(key))
                break
