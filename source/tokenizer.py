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
import re
import lexicalRules

# open example file as a string
with open('example.txt', 'r') as exampleFile:
    ex1 = exampleFile.read()

# gather list of lexemes from scanner.py
lexemes = scan(ex1)

# bool used to short circuit to reduce redundant searching
keywordFound = False

# loop through each lexeme and keep track of index
for index, lex in enumerate(lexemes):
    keywordFound = False
    # check all keywords first
    for key in lexicalRules.keywords:
        # attempt to match lex with a keyword
        x = re.search(lexicalRules.keywords[key], lex)
        if x is not None:
            print('Lexeme {}: {}'.format(index + 1, lex).ljust(25) +
                  'Token: {}'.format(key))
            keywordFound = True
            # break if found, skip to next lexeme
            break
    # if no keyword matches, check if a literal
    if not keywordFound:
        for key in lexicalRules.literals:
            y = re.search(lexicalRules.literals[key], lex)
            if y is not None:
                print('Lexeme {}: {}'.format(index + 1, lex).ljust(25) +
                      'Token: {}'.format(key))
                # break if found, skip to next lexeme
                break
